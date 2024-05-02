import requests


data = {
    "members": "150",
    "active_members": "1"
}

requests.post(
    url="http://127.0.0.1:5000/api/get_info",
    headers={
        "token": "zLjv0i6oS7JH8xiykh3LQFexcocDqEZe"
    },
    json=data
)