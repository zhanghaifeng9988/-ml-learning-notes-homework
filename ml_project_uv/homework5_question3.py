import pickle

# 1. 加载模型
with open('pipeline_v1.bin', 'rb') as f:
    pipeline = pickle.load(f)

# 2. 准备输入数据（字典）
input_data = {
    "lead_source": "paid_ads",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0
}

# 3. 预测（注意：用 [ ] 包住字典，变成字典列表）
prediction = pipeline.predict([input_data])

# 4. 输出结果
print(f"预测结果: {prediction[0]}")

# 5. 如果想看概率
probabilities = pipeline.predict_proba([input_data])
print(f"预测概率: {probabilities[0]}")