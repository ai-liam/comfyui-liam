import sys
import os
from PIL import Image, ImageOps
# import folder_paths
import torch
import numpy as np
import requests
from io import BytesIO
import cv2


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
    print(f"2 image type: {type(image)}")
    return (image, mask.unsqueeze(0))



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


# def process_image(tensor_image):
#     print(f"tensor_image type: {type(tensor_image)}")
#     # I type: <class 'torch.Tensor'>
#     # torch.Size([1, 1024, 1024, 3])
#     # 将输入的形状调整为 [height, width, channels]
#     tensor_image = tensor_image.squeeze().permute(1, 2, 0)
#     # 将 RGB 彩色图像转换为灰度图像
#     gray_image = 0.2989 * tensor_image[..., 0] + 0.5870 * tensor_image[..., 1] + 0.1140 * tensor_image[..., 2]
#     # 将灰度图像重新调整为原始形状
#     gray_image = gray_image.unsqueeze(0).permute(2, 0, 1)
#     return gray_image

def cv2_grayscale(image):
    # 将PyTorch张量转换为NumPy数组
    image_np = image.cpu().numpy()
    # 将NumPy数组转换为OpenCV格式的图像
    # 先将通道轴移动到最后一个维度
    image_np = np.moveaxis(image_np, 0, -1)
    # 将图像数据从[0,1]的范围还原到[0,255]的范围
    image_np = (image_np * 255).astype(np.uint8)
    # 使用OpenCV将图像转换为灰度图
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    # 将灰度图再转换为RGB格式的图像（因为torch.from_numpy期望的是RGB格式）
    gray_image_rgb = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
    # 将图像转换回PyTorch张量
    # 先将通道轴移动回第一个维度
    gray_image_tensor = np.moveaxis(gray_image_rgb, -1, 0)
    gray_image_tensor = torch.from_numpy(gray_image_tensor).float()
    # 将张量移回原始设备（可能是GPU）
    if image.is_cuda:
        gray_image_tensor = gray_image_tensor.cuda()
    return gray_image_tensor

def image_to_gray(i):
    print(f"I type: {type(i)}")
    print(i.shape)
    # 将 torch.Tensor 转换为 NumPy 数组
    numpy_image = i.numpy()
    # 将 RGB 图像转换为 BGR 格式，因为 OpenCV 使用 BGR 格式
    bgr_image = numpy_image.transpose(1, 2, 0)[:, :, ::-1]
    # 将 BGR 图像转换为灰度图像
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    return gray_image
    # if isinstance(i, torch.Tensor):
    #     # 对 torch.Tensor 对象进行灰度化处理
    #     # 这里简单地使用加权平均法将彩色图像转换为灰度图像
    #     # 公式为：灰度值 = 0.2989 * R + 0.5870 * G + 0.1140 * B
    #     gray_image = 0.2989 * i[:, 0, :, :] + 0.5870 * i[:, 1, :, :] + 0.1140 * i[:, 2, :, :]
    #     return gray_image
    # else:
    #     # 对于其他类型的对象，使用 PIL 库的方法进行转换
    #     i_pil = i.convert("RGB")  # 先将输入转换为 RGB 模式（如果不是）
    #     gray_image = i_pil.convert("L")  # 转换为灰度图像
    #     return gray_image
    # i = ImageOps.exif_transpose(i)
    # image = i.convert("RGB")
    # image = np.array(image).astype(np.float32) / 255.0
    # image = torch.from_numpy(image)[None,]
    # gray_image = i.convert("L")
    # return gray_image
