import sys
import os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

import lib_utils
#sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

class ImageToGray:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "image": ("IMAGE",)}}
    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "execute"
    CATEGORY = "Liam/Image"

    def execute(self,image):
        print(f"""Your input contains:
                image: {type(image)}
            """)
        img = lib_utils.convert_to_gray_and_return_tensor_pil(image)
        return (img,)
        

class LoadImage:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = path+"/../../input"
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"url": ("STRING", {"default": ""}),
                    "image": (sorted(files), {"image_upload": True})
                    },
                }
    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "execute"
    CATEGORY = "Liam/Image"

    def execute(self,url,image):
        print(f"""Your input contains:
                url: {url} ,
                img: {image}
            """)
        if  url.startswith('http'):
            i = lib_utils.open_image_from_url(url)
            return lib_utils.back_image(i)
        else:
            i = lib_utils.open_image_from_input(image)
            return lib_utils.back_image(i)



NODE_CLASS_MAPPINGS = {
    "LiamLibLoadImage": LoadImage,
    "LiamLibImageToGray": ImageToGray,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LiamLibLoadImage": "LoadImage_Liam",
    "LiamLibImageToGray": "ImageToGray_Liam",
}
