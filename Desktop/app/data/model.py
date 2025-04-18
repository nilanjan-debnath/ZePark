import tensorflow as tf

path = "app/data/resource/model/ZePark_bimodel v1.1.keras"
model = tf.keras.models.load_model(path)
