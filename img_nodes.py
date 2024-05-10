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



class PreviewReliefImage:
    @classmethod
    def INPUT_TYPES(s):
        return { "required": {
                "image": ("IMAGE",),
                "emboss_depth": ("INT", { "default": 60, "min": 0, "max": 100, "step": 1, }),
                "light_angle": ("INT", { "default": 135, "min": 0, "max": 360, "step": 1, }),
                "light_intensity": ("INT", { "default": 0.8, "min": 0, "max": 1, "step": 0.1, }),
                "edge_threshold": ("INT", { "default": 30, "min": 0, "max": 100, "step": 5, }), 
            }
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "execute"
    CATEGORY = "Liam/Image"

    def execute(self,image, emboss_depth, light_angle, light_intensity, edge_threshold):
        print(f"""Your input contains:
                image: {type(image)}
            """)
        outputs = lib_utils.preview_relief_image(image,emboss_depth, light_angle, light_intensity, edge_threshold)
        return (outputs, )


class FillImage:
    @classmethod
    def INPUT_TYPES(s):
        MAX_RESOLUTION=16384
        return { "required": {
                "image": ("IMAGE",),
                "width": ("INT", { "default": 1024, "min": 0, "max": MAX_RESOLUTION, "step": 8, }),
                "height": ("INT", { "default": 1024, "min": 0, "max": MAX_RESOLUTION, "step": 8, }),
                "red": ("INT", { "default": 255, "min": 0, "max": 255, "step": 8, }),
                "green": ("INT", { "default": 255, "min": 0, "max": 255, "step": 8, }),
                "blue": ("INT", { "default": 255, "min": 0, "max": 255, "step": 8, }),
                "alpha": ("INT", { "default": 255, "min": 0, "max": 255, "step": 1, }),  
            }
        }
    RETURN_TYPES = ("IMAGE", "INT", "INT",)
    RETURN_NAMES = ("IMAGE", "width", "height",)
    FUNCTION = "execute"
    CATEGORY = "Liam/Image"

    def execute(self,image, width, height, red, green, blue, alpha):
        print(f"""Your input contains:
                image: {type(image)}
            """)
        fill_color=(red,green,blue,alpha)
        fill_size=(width, height)
        outputs = lib_utils.fill_img_color(image,fill_color,fill_size)
        return (outputs, outputs.shape[2], outputs.shape[1],)


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
            filename_with_batch_num = filename_with_batch_num.replace('.png', '')
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1
        return { "ui": { "images": results } }
