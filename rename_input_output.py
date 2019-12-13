## Used to change the name of input and output to give a good name.

from coremltools import utils

spec = utils.load_spec("FacialExpressionAnalysis.mlmodel")
##utils.rename_feature(spec,"UglyInputName","image",rename_outputs = True)
utils.rename_feature(spec,"input.1","data",rename_inputs = True,rename_outputs = False)
#utils.rename_feature(spec,"198","result",rename_inputs = False,rename_outputs = True)
utils.save_spec(spec,"FacialExpressionAnalysis.mlmodel")
