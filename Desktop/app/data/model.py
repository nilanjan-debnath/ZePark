# TODO: for windows use tensorflow but for other os like linux or mac even in embedded devices use ai_edge_litert
# from ai_edge_litert.interpreter import Interpreter
import tensorflow as tf


def get():
    # model_path = "app/data/resource/model/ZePark_bimodel v2.256.1.tflite"
    # model_path = "app/data/resource/model/ZePark_bimodel 256x256x3.tflite"
    model_path = "app/data/resource/model/ZePark_bimodel 128x128x3.tflite"
    # interpreter = Interpreter(model_path=model_path)
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter
