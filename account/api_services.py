import requests

API_URL = "http://127.0.0.1:8000"

def create_acc(name, password, phoneNum) : 
    try : 
        data = {
            "name" : name,
            "password" : password,
            "phoneNum" : phoneNum
        }
        res = requests.post(f"{API_URL}/accounts", json = data)
        print("RAW RESPONSE:", res.text)
        return res.json()
    except Exception as e : 
        print("Create Account Error :",e)
        return None

def login_acc(name, password) : 
    try : 
        data = {
            "name" : name,
            "password" : password
        }
        res = requests.post(f"{API_URL}/login", json = data)
        return res.json() 
    except Exception as e : 
        print("Login account error :",e)
        return None
