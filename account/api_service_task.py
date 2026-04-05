import requests

API_URL = "http://127.0.0.1:8001"


def get_tasks(user_id):
    try:
        res = requests.get(f"{API_URL}/tasks/{user_id}")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Get Tasks Error:", e)
        return []


def add_task(user_id, title, description, priority, due_date, due_time):
    try:
        data = {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "due_time" : due_time,
            "completed": False
        }
        requests.post(f"{API_URL}/tasks/{user_id}", json=data)
        return True
    except Exception as e:
        print("Add Task Error:", e)
        return False


def delete_task(task_id):
    try:
        requests.delete(f"{API_URL}/tasks/{task_id}")
        return True
    except Exception as e:
        print("Delete Error:", e)
        return False


def update_task(task_id, title, description, priority, due_date, due_time, completed):
    try:
        data = {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "due_time" : due_time,
            "completed": completed
        }
        requests.put(f"{API_URL}/tasks/{task_id}", json=data)
        return True
    except Exception as e:
        print("Update Error:", e)
        return False


def search_task(user_id, keyword):
    try:
        res = requests.get(f"{API_URL}/tasks/search/{user_id}", params = {"keyword" : keyword}, timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Search Error:", e)
        return []