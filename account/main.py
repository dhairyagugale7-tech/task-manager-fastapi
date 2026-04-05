from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Dhai@281006",
    database = "task_manager2"
)

cursor = conn.cursor(dictionary = True)

app = FastAPI()

class Create(BaseModel) : 
    name : str
    password : str
    phoneNum : str

class Login(BaseModel) : 
    name : str
    password : str

account = []

@app.post("/accounts")
def create_acc(info : Create) : 
    cursor.execute("insert into users(name, password, phoneNum) values (%s, %s, %s)", (info.name, info.password, info.phoneNum))
    conn.commit()

    return {"message" : "Account created successfully...!!"}

@app.post("/login")
def login_acc(data : Login) :
    cursor.execute("select * from users where name = %s and password = %s", (data.name, data.password))
    user = cursor.fetchone()
    if user : 
        return {"message" : "Login Successfully...!!",
                "user_id" : user["id"]}
    else : 
        return {"message" : "Wrong Credentials...!!"}

