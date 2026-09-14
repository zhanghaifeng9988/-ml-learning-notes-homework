import boto3
import json

lambda_client = boto3.client('lambda')  #创建 Lambda 客户端

customer_data = {
    "customer": {
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
        "tenure": 1,
        "monthlycharges": 29.85,
        "totalcharges": 29.85
    }
}

response = lambda_client.invoke(
    FunctionName='churn-prediction-docker', # 把数据发给云上的 Lambda 函数 
    InvocationType='RequestResponse',# 同步调用,本地脚本发出请求后会等待，直到 Lambda 执行完并返回结果，才继续往下走
    Payload=json.dumps(customer_data) #
)


result = json.loads(response['Payload'].read()) #读取 Lambda 返回的预测结果
print(json.dumps(result, indent=2))

