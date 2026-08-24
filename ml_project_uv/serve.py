# serve.py

import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import Dict, Any

# 1. 加载模型
MODEL_PATH = "pipeline_v1.bin"  # 确保路径正确

try:
    with open(MODEL_PATH, "rb") as f:
        pipeline = pickle.load(f)
    print(f"✅ Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    print(f"❌ Model file not found: {MODEL_PATH}")
    print("Please ensure pipeline_v1.bin is in the current directory")
    exit(1)

# 2. 定义请求体数据结构（Pydantic 模型）
# ClientData 继承自 BaseModel，它的作用是：
# 定义数据结构：规定 API 请求体必须包含哪些字段，以及它们的类型
# 自动验证：如果传入的数据类型不对（比如 annual_income 传了字符串），它会自动报错
# 自动生成文档：FastAPI 会根据这个定义生成 Swagger 文档
class ClientData(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float
    
    # 可选：添加数据验证,为 API 文档提供一个示例数据,当你访问 /docs（Swagger UI）时，会自动填充这个示例
    class Config:
        json_schema_extra = {
            "example": {
                "lead_source": "organic_search",
                "number_of_courses_viewed": 4,
                "annual_income": 80304.0
            }
        }


# 3. 创建 FastAPI 应用
app = FastAPI(
    title="Lead Scoring Model API",
    description="Predict whether a lead will convert",
    version="1.0.0"
)

# 4. 健康检查端点
@app.get("/")
def read_root():
    return {"message": "Lead Scoring Model API is running", "status": "healthy"}

# 5. 预测端点
@app.post("/predict")
def predict(client: ClientData):
    """
    Predict conversion probability for a single client
    """
    try:
        # 将输入数据转换为字典
        input_dict = client.model_dump()  # Pydantic v2
        # 如果是 Pydantic v1，用 .dict()
        
        # 转换为字典列表（DictVectorizer 需要的格式）
        input_data = [input_dict]
        
        # 进行预测
        prediction = pipeline.predict(input_data)[0]
        
        # 获取概率（如果是分类模型）
        try:
            probability = pipeline.predict_proba(input_data)[0][1]  # 假设是二分类
        except (AttributeError, IndexError):
            probability = None
        
        # 返回结果
        response = {
            "prediction": int(prediction),
            "probability": float(probability) if probability is not None else None,
            "input_data": input_dict
        }
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9009) 

    