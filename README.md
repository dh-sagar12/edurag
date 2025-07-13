# AI Tutor Project Setup

This project uses **FastAPI** as the backend framework.

---

## 🚀 Project Setup Instructions

### 1. Python Environment

Ensure you have [pyenv](https://github.com/pyenv/pyenv) installed.

1. Install Python 3.12.6 using pyenv:

   ```bash
   pyenv install 3.12.6
   pyenv local 3.12.6
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:

   ```bash
   cp .env.template .env
   ```

   Edit the `.env` file and add your environment variables.

   ```bash
   nano .env
   ```
    * I have used gemini for chat so replace `GEMINI_API_KEY` with your own values.
    
5. 
---

### 2. Running the Application

This project uses a **Makefile** for simplified commands.

* To start the application:

  ```bash
  make start
  ```

* Alternatively, run using uvicorn directly:

  ```bash
  uvicorn main:app --reload
  ```

Your backend will run on **[http://localhost:8000](http://localhost:8000)**.

---

### 3. Swagger Documentation

Access the API documentation at:

```
http://localhost:8000/docs
```

---

### 4. Nginx Configuration (For Deployment)

1. Install nginx:

   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. The nginx configuration for this project is provided in the `nginx.conf` file. Use it to set up nginx for your application. By default, the application will be accessible on **localhost**.

---

### 5. Frontend Setup

* The pre-built `dist` folder for the frontend is included.

* To set up environment variables:

  1. Rename `.env.template` inside the `frontend` directory to `.env`.

  2. Use it as is or adjust as required.

* Visit the frontend at:

  ```
  http://localhost
  ```

---

## 📩 Contact

For any queries, feel free to contact:

* **Email:** [dhakalsagar2000@gmail.com](mailto:dhakalsagar2000@gmail.com)
* **Phone:** +977 9864414883

---

### ✅ Notes

* Ensure ports 80 and 8000 are free before starting nginx and uvicorn.

---
