# test_client.py

import requests
import json

# 服务地址
url = "http://127.0.0.1:9008/predict"

# 你的测试数据
client = {
    "lead_source": "organic_search",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0
}

# 发送 POST 请求
response = requests.post(url, json=client)

# 打印结果
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))