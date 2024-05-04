import requests


data = {
    "members": "180",
    "active_members": "100"
}

requests.post(
    url="http://127.0.0.1:5200/api/send_stats",
    headers={
        "token": "leJiekR7IqEMEBcHbZjNKcDkO7p1gMqv"
    },
    json=data
)