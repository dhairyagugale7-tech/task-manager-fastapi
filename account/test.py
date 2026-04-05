import requests

requests.post(
    "https://dhairya-7.app.n8n.cloud/webhook-test/task-reminder",
    json={
        "title": "Drink Water",
        "due_datetime": "2026-04-04 14:30:00",
        "phone": "+918208166576"
    }
)