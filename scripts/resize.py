from PIL import Image
import os, sys

path = "../data/imgs"
dirs = os.listdir(path)

resize_ratio = 0.5


def resize():
    for item in dirs:
        print(item)
        itempath = path + '/' + item
        image = Image.open(itempath)
        image = image.convert('RGB')
        file_path, extension = os.path.splitext(itempath)
        size = image.size

        new_image_height = 250
        new_image_width = int(size[1] / size[0] * new_image_height)

        image = image.resize((new_image_height, new_image_width), Image.ANTIALIAS)
        image.save(file_path + extension, 'JPEG', quality=90)


resize()
