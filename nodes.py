import sys
import os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

sys.path.append(path+"/../../")

import img_nodes
import text_nodes

#sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))


NODE_CLASS_MAPPINGS = {
    "LiamLibLoadImage": img_nodes.LoadImage,
    "LiamLibImageToGray": img_nodes.ImageToGray,
    "LiamLibSaveImg": img_nodes.MySaveImage,
    "LiamLibFillImage": img_nodes.FillImage ,

    "LiamLibSaveText": text_nodes.SaveText ,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LiamLibLoadImage": "Load Image @Liam",
    "LiamLibImageToGray": "Image To Gray @Liam",
    "LiamLibSaveImg": "Save Image @Liam",
    "LiamLibFillImage":  "Fill Image @Liam",

    "LiamLibSaveText": "Save Text @Liam",
}
