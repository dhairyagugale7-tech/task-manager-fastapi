# 🚀 Task Manager Web App

A full-stack task management application built using FastAPI, Streamlit, and MySQL.

---

## 🔹 Features

* User Authentication (Login & Signup)
* Create, Update, Delete Tasks
* Task Scheduling with Reminders (Twilio)
* Clean UI using Streamlit

---

## 🛠️ Tech Stack

* Backend: FastAPI
* Frontend: Streamlit
* Database: MySQL
* API Integration: Twilio

---

## ⚙️ Requirements

Make sure you have the following installed:

* Python 3.x
* MySQL
* pip

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/task-manager-fastapi.git
cd task-manager-fastapi
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # For Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create `.env` file

Create a file named `.env` and add:

```
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_number

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=task_manager2
```

---

### 5. Run Backend

```bash
python -m uvicorn account.main:app --reload --port 8000
```

---

### 6. Run Frontend

```bash
python -m streamlit run account/app.py
```

---

## 🌐 Usage

Open browser:

* Backend Docs: http://127.0.0.1:8000/docs
* Frontend: http://localhost:8501

---

## 📌 Note

* Twilio SMS works only for verified numbers in trial mode
* Use your own database credentials

---

## 💻 Author

Built with ❤️ by Dhairya
