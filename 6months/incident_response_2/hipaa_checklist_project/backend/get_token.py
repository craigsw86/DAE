import requests

url = "http://localhost:8000/api/token/"
data = {
    "username": "TestUsername",   # <-- use your actual username
    "password": "TestPassword"    # <-- use your actual password
}
response = requests.post(url, json=data)
print("Status code:", response.status_code)
print("Response:", response.json())