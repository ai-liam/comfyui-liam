import sys
import os
from PIL import Image, ImageOps
import folder_paths
import torch
import numpy as np
import requests
from io import BytesIO

#sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))



def open_image_from_url(url):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    image = Image.open(image_data)
    return image

def open_image_from_input(file_name):
    image_path = folder_paths.get_annotated_filepath(file_name)
    image = Image.open(image_path)
    return image

def back_image(i):
    i = ImageOps.exif_transpose(i)
    image = i.convert("RGB")
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image)[None,]
    if 'A' in i.getbands():
        mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
        mask = 1. - torch.from_numpy(mask)
    else:
        mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
    return (image, mask.unsqueeze(0))

class LiamLoadImage:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"url": ("STRING", {"default": ""}),
                    "image": (sorted(files), {"image_upload": True})},
                }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"
    CATEGORY = "image"




    def load_image(self,url, image):
        print(f"""Your input contains:
                url: {url}
                image: {image}
            """)
        if url != "" and url.startswith('http'):
            i = open_image_from_url(url)
            return back_image(i)
        else:
            i = open_image_from_input(image)
            return back_image(i)



NODE_CLASS_MAPPINGS = {
    "LiamLoadImage": LiamLoadImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LiamLoadImage": "LiamLoadImage",
}
