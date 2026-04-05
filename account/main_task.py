from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
import pytz
from dotenv import load_dotenv
import os

load_dotenv()

# Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Timezone
IST = pytz.timezone('Asia/Kolkata')

# Twilio config
import os

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms(phone, title, description):
    print("🔥 FUNCTION CALLED:", phone, title)

    try:
        message = client.messages.create(
            body=f"Reminder: {title} 💗\n description: {description}",
            from_=TWILIO_NUMBER,
            to=phone
        )
        print("✅ SMS SENT:", message.sid)

    except Exception as e:
        print("❌ SMS FAILED:", e)

def schedule_task(phone, title, description, due_datetime):
    print("⏰ Scheduling for:", due_datetime)

    scheduler.add_job(
        send_sms,
        'date',
        run_date=due_datetime,
        args=[phone, title, description]
    )

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor(dictionary = True)

app = FastAPI()
tasks = []

class Task(BaseModel) : 
    title : str
    description : str
    priority : str
    due_date : str
    due_time : str

# @app.post("/tasks/{user_id}")
# def create_task(user_id : int, task: Task):
#     cursor.execute("insert into tasks(user_id, title, des, priority, due_date, due_time, completed) values (%s,%s,%s,%s,%s,%s,%s)", (user_id, task.title, task.description, task.priority, task.due_date, task.due_time, False))
#     conn.commit()
#     return {"message" : "Task Added Successfully...!!"}

@app.post("/tasks/{user_id}")
def create_task(user_id: int, task: Task):

    # 1. Insert task into DB
    cursor.execute(
        "insert into tasks(user_id, title, des, priority, due_date, due_time, completed) values (%s,%s,%s,%s,%s,%s,%s)",
        (user_id, task.title, task.description, task.priority, task.due_date, task.due_time, False)
    )
    conn.commit()

    # 2. Get user's phone number
    cursor.execute("select phoneNum from users where id = %s", (user_id,))
    user = cursor.fetchone()

    phone = "+91" + str(user["phoneNum"])   # make sure format is +91XXXXXXXXXX
    
    # 3. Convert to datetime WITH timezone (IMPORTANT)
    due_datetime = IST.localize(datetime.strptime(
        f"{task.due_date} {task.due_time}",
        "%Y-%m-%d %H:%M:%S"
    ))

    # 4. Schedule SMS
    schedule_task(phone, task.title, task.description, due_datetime)

    return {"message": "Task Added Successfully...!!"}

# @app.post("/tasks/{user_id}")
# def create_task(user_id: int, task: Task):

#     # 🔹 Insert task into DB
#     cursor.execute(
#         "insert into tasks(user_id, title, des, priority, due_date, due_time, completed) values (%s,%s,%s,%s,%s,%s,%s)",
#         (user_id, task.title, task.description, task.priority, task.due_date, task.due_time, False)
#     )
#     conn.commit()

#     # 🔹 Get user's phone number
#     cursor.execute("select phoneNum from users where id = %s", (user_id,))
#     user = cursor.fetchone()
#     phone = "+91" + str(user["phoneNum"])

#     # 🔹 Send data to n8n webhook
#     try:
#         due_datetime = f"{task.due_date} {task.due_time}"
#         iso_time = datetime.strptime(due_datetime, "%Y-%m-%d %H:%M:%S").isoformat() + "Z"
#         requests.post(
#             "https://dhairya-7.app.n8n.cloud/webhook/task-reminder",
#             json={
#                 "title": task.title,
#                 "due_datetime": iso_time,
#                 "phone": phone
#             }
#         )
#     except Exception as e:
#         print("n8n error:", e)

#     return {"message": "Task Added Successfully...!!"}


@app.get("/tasks/{user_id}")
def get_tasks(user_id: int):
    cursor.execute("select * from tasks where user_id = %s", (user_id,))
    return cursor.fetchall()

@app.put("/tasks/{task_id}")
def update_task(update_task: Task, task_id: int):
    cursor.execute("update tasks set title = %s, des = %s, priority = %s, due_date = %s, due_time = %s where id = %s",(update_task.title, update_task.description, update_task.priority, update_task.due_date, update_task.due_time, task_id))
    conn.commit()

    return {
        "message": "Task Updated Successfully!"
    }

@app.delete("/tasks/{task_id}")
def delete_task(task_id : int) : 
    cursor.execute("delete from tasks where id = %s", (task_id,))
    conn.commit()
    return {"message" : "Task Deleted...!"}

@app.get("/tasks/search/{user_id}")
def search_task(user_id : int, keyword : str) : 
    cursor.execute("select * from tasks where user_id = %s and title like %s",(user_id, f"%{keyword}%"))
    return cursor.fetchall()

