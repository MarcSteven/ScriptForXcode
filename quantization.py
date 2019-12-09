import sys
import coremltools
from coremltools.models.neural_network.quantization_utils import *


def quantize(file,bits,functions):

    """
    processes a file to quantize it for each bit_per-weight
    and function listed.
    def quantize(file, bits, functions):
    
    Processes a file to quantize it for each bit-per-weight 
    and function listed.
    file : Core ML file to process (example : mymodel.mlmodel)
    bits : Array of bit per weight (example : [16,8,6,4,2,1])
    functions : Array of distribution functions (example : ["linear", "linear_lut", "kmeans"])
    """
    if not file.endswith(".mlmodel"): return # We only consider .mlmodel files
    model_name = file.split(".")[0]
    model = coremltools.models.MLModel(file)
    for function in functions :
        for bit in bits:
            print("--------------------------------------------------------------------")
            print("Processing "+model_name+" for "+str(bit)+"-bits with "+function+" function")
            sys.stdout.flush()
            quantized_model = quantize_weights(model, bit, function)
            sys.stdout.flush()
            quantized_model.author = "Alexis Creuzot" 
            quantized_model.short_description = str(bit)+"-bit per quantized weight, using "+function+"."
            quantized_model.save(model_name+"_"+function+"_"+str(bit)+".mlmodel")

# Launch quantization
quantize("CNNEmotions.mlmodel", 
        [6,4,3,2], 
        ["linear"])
