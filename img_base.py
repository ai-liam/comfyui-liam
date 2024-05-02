import sys
import os
import numpy as np
from PIL import Image

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

sys.path.append(path+"/../../")

import lib_utils
import lib_img
import folder_paths



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
        print(f""" LoadImage Your input contains:
                url: {url} ,
                img: {image}
            """)
        if  url.startswith('http'):
            i = lib_utils.open_image_from_url(url)
            return lib_utils.back_image(i)
        else:
            i = lib_utils.open_image_from_input(image)
            return lib_utils.back_image(i)
        

class MySaveImage:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory() #path+"/../../output"
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"images": ("IMAGE", ),
                     "filename_prefix": ("STRING", {"default": "ComfyUI"})},
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }
    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Liam/image"
    def save_images(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1
        return { "ui": { "images": results } }
