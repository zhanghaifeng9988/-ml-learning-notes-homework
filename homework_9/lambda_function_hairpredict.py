import onnxruntime as ort
import numpy as np

from io import BytesIO
from urllib import request
from PIL import Image
from keras_image_helper import create_preprocessor


def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


onnx_model_path = "hair_classifier_v1.onnx"
session = ort.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])
inputs = session.get_inputs() 
outputs = session.get_outputs() 
input_name = inputs[0].name
output_name = outputs[0].name


# 创建一个基于 Xception 模型的图像预处理流程，并把输入图像统一调整到 200×200 大小
preprocessor = create_preprocessor('xception', target_size=(200, 200))


def lambda_handler(event, context):
    X = preprocessor.from_url(event['url']) 

    X = np.transpose(X, (0, 3, 1, 2))

    result = session.run([output_name], {input_name: X})
    # 取出 logit（标量）
    logit = float(result[0][0][0])
    # sigmoid
    prob = 1 / (1 + np.exp(-logit))
    # 按 0.5 阈值判断类别
    predicted = 1 if prob > 0.5 else 0
    return {
        "predicted": predicted,
        "prob": prob,
    }



