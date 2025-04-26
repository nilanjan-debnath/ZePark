import tensorflow as tf

interpreter = None


def set_model():
    global interpreter
    model_path = "app/data/resource/model/ZePark_bimodel v1.256.3.tflite"
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()


def get():
    global interpreter
    if not interpreter:
        set_model()
    return interpreter
