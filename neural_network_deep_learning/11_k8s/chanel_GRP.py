import grpc

import tensorflow as tf

from tensorflow_serving.apis import predict_pb2 
from tensorflow_serving.apis import prediction_service_pb2_grpc

host = 'localhost:8500'

channel = grpc.insecure_channel(host)

stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

