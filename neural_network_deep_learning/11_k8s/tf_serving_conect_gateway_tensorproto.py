import numpy as np
import grpc
from flask import Flask, request, jsonify
from tensorflow_serving.apis import predict_pb2  # 用来构造发给 Serving 的预测请求
from tensorflow_serving.apis import prediction_service_pb2_grpc
from keras_image_helper import create_preprocessor
from tensorflow.core.framework import tensor_pb2, tensor_shape_pb2, types_pb2


host = 'localhost:8500'

channel = grpc.insecure_channel(host) #创建通道

stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)  

preprocessor = create_preprocessor('xception', target_size=(299, 299))

def dtypes_as_dtype(dtype):
    if dtype == "float32":
        return types_pb2.DT_FLOAT
    raise Exception("dtype %s is not supported" % dtype)


def make_tensor_proto(data):
    shape = data.shape
    dims = [tensor_shape_pb2.TensorShapeProto.Dim(size=i) for i in shape]
    proto_shape = tensor_shape_pb2.TensorShapeProto(dim=dims)

    proto_dtype = dtypes_as_dtype(data.dtype)

    tensor_proto = tensor_pb2.TensorProto(dtype=proto_dtype, tensor_shape=proto_shape)
    tensor_proto.tensor_content = data.tostring()

    return tensor_proto


def np_to_protobuf(data):
    if data.dtype != "float32":
        data = data.astype("float32")
    return make_tensor_proto(data)


    
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



app = Flask('gateway_tensorproto')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()
    url = data['url']
    result = predict(url)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)