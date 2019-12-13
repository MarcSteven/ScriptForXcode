#//
#//  convert_input_to_image.py
#//  AntsFaceDemo
#//
#//  Created by Marc Zhao on 2019/12/12.
#//  Copyright © 2019 AntsNetwork. All rights reserved.
#//

import coremltools
import coremltools.proto.FeatureTypes_pb2 as ft


spec = coremltools.utils.load_spec("FacialExpressionAnalysis.mlmodel")

input = spec.description.input[0]
input.type.imageType.colorSpace  = ft.ImageFeatureType.RGB
input.type.imageType.height = 224
input.type.imageType.width = 224

coremltools.utils.save_spec(spec,"FacialExpressionAnalysis.mlmodel")

