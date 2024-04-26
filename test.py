import requests


data = {
    "members": "150"
}

requests.post(
    url="http://127.0.0.1:5000/api/get_info",
    headers={
        "token": "QvuGeQODvuxjoUxwAysQTqjxheoKpOWu"
    },
    json=data
)