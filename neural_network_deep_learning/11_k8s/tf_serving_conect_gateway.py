import numpy as np
import tensorflow as tf
import grpc
from flask import Flask, request, jsonify
from tensorflow_serving.apis import predict_pb2  # 用来构造发给 Serving 的预测请求
from tensorflow_serving.apis import prediction_service_pb2_grpc
from keras_image_helper import create_preprocessor

host = 'localhost:8500'

channel = grpc.insecure_channel(host) #创建通道

stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)  

preprocessor = create_preprocessor('xception', target_size=(299, 299))

def np_to_protobuf(data):
    return tf.make_tensor_proto(data, shape=data.shape)
    
classes = [
    'dress',
    'hat',
    'longsleeve',
    'outwear',
    'pants',
    'shirt',
    'shoes',
    'shorts',
    'skirt',
    't-shirt'
]

# 准备请求数据
def prepare_request(X):
    pb_request = predict_pb2.PredictRequest()

    pb_request.model_spec.name = 'clothing_model'
    pb_request.model_spec.signature_name = 'serving_default'

    pb_request.inputs['input_2'].CopyFrom(np_to_protobuf(X))
    return pb_request

# 准备响应数据
def prepare_response(pb_response):
    preds = pb_response.outputs['dense_1'].float_val
    return dict(zip(classes, preds))

# 预测方法
def predict(url):
    X = preprocessor.from_url(url)
    pb_request = prepare_request(X)
    pb_response = stub.Predict(pb_request, timeout=20.0)
    response = prepare_response(pb_response)
    return response



app = Flask('gateway')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()
    url = data['url']
    result = predict(url)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)