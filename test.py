import requests

url = 'http://127.0.0.1:8000/profiles'
files = [('picture', open('./a.txt', 'rb'))]
data = {'data': '{"username": "ui","name": "Mehdi","email": "mehdi@gmail.com","birthdate": "2000-11-05","gender":"Male","bio": "Im software engineer! nice!","access_token": "5556"}'}
resp = requests.post(url=url, data=data, files=files) 
print(resp.json())