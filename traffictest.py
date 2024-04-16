import requests
import time
import random
delay=1

print("Running Test\nSimulating Network Traffic")

for i in range(200):
    payload = {
    'csrf_token':'fZAtAjBNrzHhz2clCJM1UAignNuRx2yJ',
    'business_name' : 'something',
    'email' : f'magudesh200{i}@gmail.com',
    'password1' : 'senbagam',
    'password2' : 'senbagam'
}
    a=requests.post("http://127.0.0.1:8000/auth/signup/",data=payload)
    print(f"Request {i}, {a.status_code}")
