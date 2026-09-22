import requests

# url = 'http://127.0.0.1:9696/predict'
url = 'http://127.0.0.1:8080/predict'
image_url = {"url": "https://pic.mksucai.com/00/10/42/60e8c5905c7695a3.webp"}

response = requests.post(url, json=image_url)      

print("状态码:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("响应体:")
print(response.text)
