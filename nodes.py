import sys
import os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

sys.path.append(path+"/../../")

import img_base
import text_nodes

#sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))


NODE_CLASS_MAPPINGS = {
    "LiamLibLoadImage": img_base.LoadImage,
    "LiamLibImageToGray": img_base.ImageToGray,
    "LiamLibSaveImg": img_base.MySaveImage,
    "LiamLibSaveText": text_nodes.SaveText ,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LiamLibLoadImage": "Load Image @Liam",
    "LiamLibImageToGray": "Image To Gray @Liam",
    "LiamLibSaveImg": "Save Image @Liam",
    "LiamLibSaveText": "Save Text @Liam",
}
