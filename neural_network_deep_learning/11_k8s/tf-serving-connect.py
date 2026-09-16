#!/usr/bin/env python
# coding: utf-8

#Autosave disabled
get_ipython().run_line_magic('autosave', '0')


import numpy as np
import tensorflow as tf
import grpc
from tensorflow_serving.apis import predict_pb2  # 用来构造发给 Serving 的预测请求
from tensorflow_serving.apis import prediction_service_pb2_grpc


from keras_image_helper import create_preprocessor  #图像预处理器
host = 'localhost:8500'

channel = grpc.insecure_channel(host) #创建通道

stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)   


preprocessor = create_preprocessor('xception', target_size=(299, 299)) 


url = 'https://pic.mksucai.com/00/10/42/60e8c5905c7695a3.webp'
X = preprocessor.from_url(url)


def np_to_protobuf(data):
    return tf.make_tensor_proto(data, shape=data.shape)


pb_request = predict_pb2.PredictRequest()

pb_request.model_spec.name = 'clothing-model'
pb_request.model_spec.signature_name = 'serving_default'

pb_request.inputs['input_2'].CopyFrom(np_to_protobuf(X))


pb_response = stub.Predict(pb_request, timeout=20.0)



preds = pb_response.outputs['dense_1'].float_val


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


dict(zip(classes, preds))


