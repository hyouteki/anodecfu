import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import LSTM

def usage():
    print("usage: tfliteutils [SUBCOMMAND] <ARGS>")
    print()
    print("SUBCOMMAND:")
    print("    from_keras     <modelpath>")
    print("    estimate_size  <modelpath>")
    print("    help")

def error(message, show_usage: bool = True):
    print(f"error: {message}")
    if show_usage:
        usage()
    exit(1)
    
if len(sys.argv) < 2:
    error("no subcommand found")

subcommand = sys.argv[1]

if subcommand == "help":
    usage()
    exit(0)

class CustomLSTM(LSTM):
    def __init__(self, *args, **kwargs):
        # Remove "time_major" if present to prevent errors
        kwargs.pop("time_major", None)
        super().__init__(*args, **kwargs)
    
def from_keras_helper(modelpath):
    model = tf.keras.models.load_model(modelpath)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    open(modelpath.replace("h5", "tflite"), "wb").write(tflite_model)

def from_keras(modelpath):
    try:
        from_keras_helper(modelpath)
        return
    except:
        pass
    
    custom_objects = {"LSTM": CustomLSTM}
    try:
        model = tf.keras.models.load_model(modelpath, custom_objects=custom_objects)
    except Exception as e:
        error(f"could not load model: {e}", False)
    
    try:
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.target_spec.supported_ops = [
            tf.lite.OpsSet.TFLITE_BUILTINS,
            tf.lite.OpsSet.SELECT_TF_OPS
        ]
        
        # Disable lowering tensor list ops
        # Note: _experimental_lower_tensor_list_ops is an internal flag.
        # Accessing it directly may raise warnings, but it"s necessary here.
        setattr(converter, "_experimental_lower_tensor_list_ops", False)
        # Enable resource variables
        converter.experimental_enable_resource_variables = True
        # Optional: Optimize the model (e.g., for size or latency)
        # converter.optimizations = [tf.lite.Optimize.DEFAULT]

        tflite_model = converter.convert()
    except Exception as e:
        error(f"could not convert model to tflite: {e}", False)
    
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
    print(f"info: total estimated memory: '{total_memory} B'")

if len(sys.argv) < 3:
    error("no <modelpath> arg found")
    
modelpath = sys.argv[2]

if subcommand == "from_keras":
    from_keras(modelpath)
elif subcommand == "estimate_size":
    estimate_size(modelpath)
else:
    error(f"invalid subcommand '{subcommand}'")
