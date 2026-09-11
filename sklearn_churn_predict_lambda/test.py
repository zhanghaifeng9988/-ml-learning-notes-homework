import requests
import json
# 它是 AWS Lambda 运行时接口（RIC）的标准调用地址
url = 'http://localhost:9999/2015-03-31/functions/function/invocations'

customer = {
    "gender": "female",
    "seniorcitizen": 0,
    "partner": "yes",
    "dependents": "no",
    "phoneservice": "no",
    "multiplelines": "no_phone_service",
    "internetservice": "dsl",
    "onlinesecurity": "no",
    "onlinebackup": "yes",
    "deviceprotection": "no",
    "techsupport": "no",
    "streamingtv": "no",
    "streamingmovies": "no",
    "contract": "month-to-month",
    "paperlessbilling": "yes",
    "paymentmethod": "electronic_check",
    "tenure": 24,
    "monthlycharges": 29.85,
    "totalcharges": (24 * 29.85)
}

#with open('customer.json', 'r') as f_in:   
#    customer = json.load(f_in)

result = requests.post(url, json={"customer": customer}).json()
print(result)
