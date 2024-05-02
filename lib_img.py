
import sys
import os
from PIL import Image
import numpy as np


# 将RGB图像转换为灰度图像
def save_img(image_tensor,output_path,fname):
    # 将torch.Tensor转换为numpy数组
    image = image_tensor.numpy().squeeze()
    # 将numpy数组转换为PIL图像
    image = Image.fromarray((image * 255).astype(np.uint8))
    # 将RGB图像转换为灰度图像
    image = image.convert("L")
    # 将灰度图像复制到3个通道，使其看起来像RGB图像
    image = Image.merge("RGB", (image, image, image))
    # is check the output path exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # save the image
    file_path = os.path.join(output_path,fname)
    image.save(file_path)


def get_save_image_path(filename_prefix, output_dir, image_width=0, image_height=0):
    def map_filename(filename):
        prefix_len = len(os.path.basename(filename_prefix))
        prefix = filename[:prefix_len + 1]
        try:
            digits = int(filename[prefix_len + 1:].split('_')[0])
        except:
            digits = 0
        return (digits, prefix)

    def compute_vars(input, image_width, image_height):
        input = input.replace("%width%", str(image_width))
        input = input.replace("%height%", str(image_height))
        return input

    filename_prefix = compute_vars(filename_prefix, image_width, image_height)

    subfolder = os.path.dirname(os.path.normpath(filename_prefix))
    filename = os.path.basename(os.path.normpath(filename_prefix))

    full_output_folder = os.path.join(output_dir, subfolder)

    if os.path.commonpath((output_dir, os.path.abspath(full_output_folder))) != output_dir:
        err = "**** ERROR: Saving image outside the output folder is not allowed." + \
              "\n full_output_folder: " + os.path.abspath(full_output_folder) + \
              "\n         output_dir: " + output_dir + \
              "\n         commonpath: " + os.path.commonpath((output_dir, os.path.abspath(full_output_folder)))
        # logging.error(err)
        raise Exception(err)

    try:
        counter = max(filter(lambda a: a[1][:-1] == filename and a[1][-1] == "_", map(map_filename, os.listdir(full_output_folder))))[0] + 1
    except ValueError:
        counter = 1
    except FileNotFoundError:
        os.makedirs(full_output_folder, exist_ok=True)
        counter = 1
    return full_output_folder, filename, counter, subfolder, filename_prefix