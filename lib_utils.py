import sys
import os
from PIL import Image, ImageOps
# import folder_paths
import torch
import numpy as np
import requests
from io import BytesIO
import cv2


path = os.path.dirname(os.path.realpath(__file__))

def open_image_from_url(url):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    image = Image.open(image_data)
    return image

def open_image_from_input(file_name):
    image_path = path+"/../../input/"+file_name
    #folder_paths.get_annotated_filepath(file_name)
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
    print(f"2 image type: {type(image)}")
    return (image, mask.unsqueeze(0))


# 将RGB图像转换为灰度图像
def convert_to_gray_and_return_tensor_pil(image_tensor):
    # 将torch.Tensor转换为numpy数组
    image = image_tensor.numpy().squeeze()
    # 将numpy数组转换为PIL图像
    image = Image.fromarray((image * 255).astype(np.uint8))
    # 将RGB图像转换为灰度图像
    image = image.convert("L")
    # 将灰度图像复制到3个通道，使其看起来像RGB图像
    image = Image.merge("RGB", (image, image, image))
    # 将PIL图像转换回numpy数组
    image = np.array(image).astype(np.float32) / 255.0
    # 将numpy数组转换回torch.Tensor
    image_tensor = torch.from_numpy(image)[None,]
    return image_tensor

