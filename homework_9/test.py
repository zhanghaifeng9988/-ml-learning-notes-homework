import requests
import json

# 本地 Lambda 容器的调用端点
url = "http://localhost:9000/2015-03-31/functions/function/invocations"

# 要传给 lambda_handler(event, context) 的 event 内容
event = {
    "url": "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
}

# 发送 POST 请求，body 就是 event 的 JSON
response = requests.post(url, json=event)

# 打印状态码和返回内容
print("Status code:", response.status_code)
print("Response body:", response.text)

# 如果返回的是 JSON，可以解析后打印
try:
    print("Parsed JSON:", json.dumps(response.json(), indent=2))
except ValueError:
    print("Response is not JSON")