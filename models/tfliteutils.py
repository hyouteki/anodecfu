import sys
import numpy as np
import tensorflow as tf

def usage():
    print("usage: tfliteutils [SUBCOMMAND] <ARGS>")
    print()
    print("SUBCOMMAND:")
    print("    from_keras     <modelpath>")
    print("    estimate_size  <modelpath>")
    print("    help")

def error(message):
    print(f"error: {message}")
    usage()
    exit(1)
    
if len(sys.argv) < 2:
    error("no subcommand found")

subcommand = sys.argv[1]

if subcommand == "help":
    usage()
    exit(0)

def from_keras(modelpath):
    model = tf.keras.models.load_model(modelpath)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    open(modelpath.replace("h5", "tflite"), "wb").write(tflite_model)

def estimate_size(modelpath):
    interpreter = tf.lite.Interpreter(model_path=modelpath)
    interpreter.allocate_tensors()
    tensor_details = interpreter.get_tensor_details()
    total_memory = 0
    for tensor in tensor_details:
        # Assuming float32 (4 bytes per element)
        tensor_size = np.prod(tensor["shape"])*4 
        total_memory += tensor_size
    print(f"info: total estimated memory: {total_memory} B")

if len(sys.argv) < 3:
    error("no <modelpath> arg found")
    
modelpath = sys.argv[2]

if subcommand == "from_keras":
    from_keras(modelpath)
elif subcommand == "estimate_size":
    estimate_size(modelpath)
else:
    error(f"invalid subcommand '{subcommand}'")
