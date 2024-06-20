import sys
import os
import numpy as np
from PIL import Image

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

sys.path.append(path+"/../../")
import lib_utils

class SaveText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "text": ("STRING", {"forceInput": True}),
                "directory": ("STRING", {"default": "tmptxt"}),
                "file_name": ("STRING", {"default": "name.txt"}),
                         },
                
            }
    RETURN_TYPES = ( "STRING",)
    FUNCTION = "execute"
    CATEGORY = "Liam/text"
    def execute(self,text,directory,file_name):
        print(f"""SaveText Your input contains:
                name: {file_name}
            """)
        _path = path+"/../../output/"+directory
        if not os.path.exists(_path):
            os.makedirs(_path)
        file_path = _path+"/"+file_name
        lib_utils.write_txt(file_path,text)
        # print(f"Text saved at: {file_path}")
        return {"ui": {"text": text}, "result": (text,)}
    

class MergeText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "text1": ("STRING", {"multiline": True, "default":"" , "dynamicPrompts": False}),
                "text2": ("STRING", {"default": "," , "multiline": True, "dynamicPrompts": False}),
                "text3": ("STRING", {"default": "", "multiline": True,"dynamicPrompts": False}),
                         },
            }
    RETURN_TYPES = ( "STRING",)
    FUNCTION = "execute"
    CATEGORY = "Liam/text"
    def execute(self,text1,text2,text3):
        text = text1+text2+text3
        return {"ui": {"text": text}, "result": (text,)}
    
class DisplayText:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {        
                "text": ("STRING", {"forceInput": True}),     
                },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
            }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "execute"

    CATEGORY = "Liam/text"

    def execute(self, text, prompt=None, extra_pnginfo=None):
        return {"ui": {"string": [text,]}, "result": (text,)}