from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_NAME")
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

