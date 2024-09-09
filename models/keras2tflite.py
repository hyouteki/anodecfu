import sys
import tensorflow as tf

if len(sys.argv) < 2:
    print("error: expected keras model (.h5) path")
    exit(1)

modelpath = sys.argv[1]

model = tf.keras.models.load_model(modelpath)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
open(modelpath.replace("h5", "tflite"), "wb").write(tflite_model)
