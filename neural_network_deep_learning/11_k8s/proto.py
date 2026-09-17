# 把一个 NumPy 数组转换成 TensorFlow 的 TensorProto 协议缓冲区（protobuf）对象。
# types_pb2	定义数据类型枚举，如 DT_FLOAT、DT_INT32 等
# tensor_shape_pb2	定义张量的形状（TensorShapeProto）
# tensor_pb2	定义张量本身（TensorProto），包含 dtype、shape、数据内容


from tensorflow.core.framework import tensor_pb2, tensor_shape_pb2, types_pb2

# 把字符串形式的 dtype 转换成 protobuf 枚举值。
def dtypes_as_dtype(dtype):
    if dtype == "float32":
        return types_pb2.DT_FLOAT
    raise Exception("dtype %s is not supported" % dtype)

# 核心转换函数，data 是一个 NumPy 数组。
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