import requests
import json

# Test login
url = 'http://localhost:8000/api/auth/login/'
data = {
    'username': 'testuser',
    'password': 'testpass123'
}

response = requests.post(url, json=data)
print(f'Status Code: {response.status_code}')
print(f'Response: {response.text}')
