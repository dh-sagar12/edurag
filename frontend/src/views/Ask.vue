<template>
    <div class="chat-container">
        <h2>Ask AI</h2>

        <!-- Persona Selector -->
        <div class="persona-select">
            <label for="persona">Select Persona:</label>
            <select v-model="selectedPersona" id="persona">
                <option value="friendly">Friendly</option>
                <option value="strict">Strict</option>
                <option value="humorous">Humorous</option>
            </select>
        </div>

        <!-- Chat Box -->
        <div class="chat-box">
            <div v-for="chat in chats" :key="chat.id" class="chat-message">
                <div class="message user-message">
                    <div class="bubble user-bubble">
                        {{ chat.user_question }}
                    </div>
                </div>
                <div class="message ai-message ">
                    <div class="bubble ai-bubble">
                        <div class="persona">
                            {{ chat.persona }}
                        </div>
                        {{ chat.ai_response }}
                    </div>
                </div>
            </div>

            <!-- Typing indicator -->
            <div v-if="loading" class="typing-indicator ai-message">
                <div class="bubble ai-bubble">AI is typing...</div>
            </div>
        </div>

        <!-- Ask Form -->
        <form @submit.prevent="askQuestion" class="ask-form">
            <div class="flex flex-col">
                <label class="switch">
                    <input type="checkbox" v-model="isSql">
                    <span class="slider round"></span>
                </label>
                <span>Query Db</span>
            </div>
            <input type="text" v-model="newQuestion" placeholder="Type your question..." :disabled="loading" required />
            <button type="submit" :disabled="loading">Ask</button>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { API_URL } from '../config'

const chats = ref([])
const newQuestion = ref('')
const isSql = ref(false)
const selectedPersona = ref('friendly')
const loading = ref(false)

const route = useRoute()
const contextId = route.query.context_id || null

const fetchChats = async () => {
    try {
        const response = await axios.get(`${API_URL}/api/v1/query-log`)
        chats.value = response.data
    } catch (err) {
        console.error(err)
    }
}

const askQuestion = async () => {
    loading.value = true
    try {
        const params = new URLSearchParams()
        params.append('question', newQuestion.value)
        params.append('persona', selectedPersona.value)
        params.append('nl_sql', isSql.value)
        if (contextId) {
            params.append('context_id', contextId)
        }

        const response = await axios.post(
            `${API_URL}/api/v1/ask?${params.toString()}`
        )

        // Append new chat to chats list
        chats.value.push({
            id: Date.now(), // Temporary ID for UI
            user_question: newQuestion.value,
            persona: selectedPersona.value,
            ai_response: response.data.answer || 'No response.',
            created_at: new Date().toISOString(),
        })

        newQuestion.value = ''
    } catch (err) {
        console.error(err)
        alert('Failed to get response. Please try again.')
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchChats()
})
</script>

<style scoped>
.chat-container {
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    flex-direction: column;
    height: 90vh;
}

h2 {
    text-align: center;
    margin-bottom: 10px;
}

.persona {
    font-size: medium;
    padding-bottom: 3px;
    color: blue;
    text-decoration: underline;
}

.persona-select {
    text-align: center;
    margin-bottom: 10px;
}

.persona-select select {
    padding: 8px;
    font-size: 14px;
}

.chat-box {
    flex: 1;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    overflow-y: auto;
    background: #f0f2f5;
    display: flex;
    flex-direction: column;
}

.chat-message {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
}

.message {
    display: flex;
}

.user-message {
    justify-content: flex-end;
}

.ai-message {
    justify-content: flex-start;
}

.bubble {
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 20px;
    margin: 2px 0;
    word-wrap: break-word;
}

.user-bubble {
    background-color: #0078fe;
    color: white;
    border-bottom-right-radius: 0;
}

.ai-bubble {
    background-color: #e4e6eb;
    color: #333;
    border-bottom-left-radius: 0;
}

.typing-indicator .ai-bubble {
    font-style: italic;
}

.ask-form {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}

.ask-form input[type="text"] {
    flex: 1;
    padding: 10px;
    font-size: 14px;
    border-radius: 20px;
    border: 1px solid #ccc;
    outline: none;
}

.ask-form button {
    padding: 10px 20px;
    background-color: #0078fe;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
}

.ask-form button:disabled {
    background-color: #94a3b8;
    cursor: not-allowed;
}
</style>