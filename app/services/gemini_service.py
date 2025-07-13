from typing import (
    Optional,
    Tuple,
    Dict,
    List,
    Any,
)
from app.models.content import Content
from app.services.embedding_service import EmbeddingService
import google.generativeai as genai
from app.config.settings import get_settings
import logging
from fastapi import HTTPException
from sqlalchemy import text
from app.models.query_log import QueryLog
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        self.schema_context = """
        Database Schema for AI Tutoring System:
        
        Table: contents
        - id (INTEGER, PRIMARY KEY): Unique identifier for content
        - title (STRING): Title of the educational content
        - topic (STRING): Subject/topic of the content
        - grade (STRING): Grade level (e.g., 'Grade 5', 'High School')
        - content (TEXT): Full text content
        - file_name (STRING): Original file name
        - chunk_count (INTEGER): Number of chunks created from this content
        - created_at (DATETIME): When content was uploaded
        - updated_at (DATETIME): When content was last modified
        
        Table: content_chunks
        - id (INTEGER, PRIMARY KEY): Unique identifier for chunk
        - content_id (INTEGER): Foreign key to contents table
        - chunk_text (TEXT): Text content of the chunk
        - chunk_index (INTEGER): Index of chunk within the content
        - embedding_vector (JSON): Vector embedding (stored as JSON)
        - created_at (DATETIME): When chunk was created
        
        Table: query_logs
        - id (INTEGER, PRIMARY KEY): Unique identifier for query
        - user_question (TEXT): Student's original question
        - ai_response (TEXT): AI tutor's response
        - persona (STRING): Tutor persona used
        - response_time (FLOAT): Time taken to generate response
        - retrieved_chunks (INTEGER): Number of chunks retrieved
        - created_at (DATETIME): When query was made
        
        Common Queries:
        - Topics by grade: SELECT DISTINCT topic FROM contents WHERE grade = 'Grade X'
        - Content count: SELECT COUNT(*) FROM contents
        - Popular topics: SELECT topic, COUNT(*) FROM contents GROUP BY topic ORDER BY COUNT(*) DESC
        - Recent queries: SELECT COUNT(*) FROM query_logs WHERE created_at > NOW() - INTERVAL '24 hours'
        """

    def generate_content(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text

    def generate_sql_query(
        self,
        nl_question: str,
    ) -> str:
        """Convert natural language to SQL query"""
        system_prompt = f"""You are a SQL expert. Convert natural language questions to SQL queries.
        
        Database Schema:
        {self.schema_context}
        
        Rules:
        1. Return only the SQL query, no explanations
        2. Use proper PostgreSQL syntax
        3. Be careful with table and column names
        4. For counting, use COUNT(*)
        5. For filtering, use proper WHERE conditions
        """

        try:
            full_prompt = f"{system_prompt}\n\nQuestion: {nl_question}"

            response = self.generate_content(full_prompt)
            return response
        except Exception as e:
            logger.error(f"Error generating SQL: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate SQL query",
            )

    def generate_context_based_response(
        self,
        question: str,
        persona: str,
        db: Session,
        context_id: Optional[int] = None,
    ) -> str:
        """Generate context based response"""
        try:
            vector_store = EmbeddingService()
            matched_ids = vector_store.search(question)

            # Retrieve matched contents from DB
            if context_id:
                contents = (
                    db.query(Content)
                    .filter(
                        Content.id == context_id,
                    )
                    .all()
                )
            else:
                contents = (
                    db.query(Content)
                    .filter(
                        Content.id.in_(matched_ids),
                    )
                    .all()
                )

            contexts = [content.content for content in contents]
            combined_context = "\n".join(contexts)

            # Persona prompt variations
            persona_instructions = {
                "friendly": "Respond in a kind and encouraging way.",
                "strict": "Respond strictly and directly without any casual tone.",
                "humorous": "Add a slight touch of humor to make learning fun.",
            }
            persona_prompt = persona_instructions.get(
                persona.lower(), persona_instructions["friendly"]
            )

            # Generate Gemini answer
            prompt = f"""
            You are an educational tutor. {persona_prompt}

            Use this context to answer clearly for students. If you couldn't find the answer in the context, respond with "I don't know, It is out of context question.".

            Context: {combined_context}

            Question: {question}

            Answer:
            """
            response = self.generate_content(prompt)

            # save respone to the db for query log
            query_log = QueryLog(
                user_question=question,
                persona=persona,
                ai_response=response,
            )
            db.add(query_log)
            db.commit()
            return {
                "persona": persona,
                "answer": response,
            }
        except Exception as e:
            logger.error(f"Error asking question: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to give answer",
            )

    def process_nl_query(
        self,
        nl_question: str,
        persona: str,
        db: Session,
    ) -> Tuple[str, str, List[Dict[str, Any]]]:
        """Process natural language query and return SQL + results"""
        try:
            # Generate SQL query
            sql_query = self.generate_sql_query(
                nl_question=nl_question,
            )

            # Clean up the SQL query (remove markdown formatting if present)
            sql_query = sql_query.strip()
            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:]
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]
            sql_query = sql_query.strip()
            logger.info(f"Generated SQL query: {sql_query}")

            # Execute the query
            result = db.execute(text(sql_query))

            # Convert results to list of dictionaries
            columns = result.keys()
            data = []
            for row in result:
                data.append(dict(zip(columns, row)))

            # Generate human-readable answer
            answer = self._generate_human_readable_answer(
                question=nl_question,
                sql_query=sql_query,
                persona=persona,
                data=data,
            )
            query_log = QueryLog(
                user_question=nl_question,
                persona=persona,
                ai_response=answer,
            )
            db.add(query_log)
            db.commit()

            return {
                "persona": persona,
                "answer": answer,
            }

        except Exception as e:
            logger.error(f"Error processing NL query: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to process NL query",
            )

    def _generate_human_readable_answer(
        self,
        question: str,
        sql_query: str,
        persona: str,
        data: List[Dict[str, Any]],
    ) -> str:
        """Generate a human-readable answer from SQL results"""
        try:

            # Persona prompt variations
            persona_instructions = {
                "friendly": "Respond in a kind and encouraging way.",
                "strict": "Respond strictly and directly without any casual tone.",
                "humorous": "Add a slight touch of humor to make learning fun.",
            }
            persona_prompt = persona_instructions.get(
                persona.lower(), persona_instructions["friendly"]
            )

            system_prompt = f"""You are a helpful assistant that explains database query results in natural language.
            {persona_prompt}
            Given a user's question, the SQL query used to answer it, and the results, provide a clear, 
            conversational explanation of what the data shows.            
            If there are multiple results, summarize them appropriately.
            """

            user_message = f"""
            Question: {question}
            SQL Query: {sql_query}
            Results: {data}
            
            Please provide a natural language explanation of these results.
            """

            full_prompt = (
                f"{system_prompt}\n\nQuestion: {user_message}"
            )

            response = self.generate_content(
                full_prompt,
            )

            return response

        except Exception as e:
            logger.error(f"Error generating human-readable answer: {e}")
            return f"Found {len(data)} results for your query."
