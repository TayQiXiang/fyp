import os
import numpy as np
import json
from sklearn.model_selection import train_test_split
from PIL import Image
import shutil
import random

folder_dir = r'data/imagenet/image'
if not os.path.exists(folder_dir):
    print("Folder does not exist")
    exit()
for root, dirs, files in os.walk(folder_dir):
    for file in files:

        if file.endswith("png") or file.endswith("PNG") or file.endswith("jpg") or file.endswith("JPG") or file.endswith("jpeg") or file.endswith("JPEG"):
            
            # resize the image to 256x256
            image_path = os.path.join(root, file)
            img = Image.open(image_path)
            img = img.resize((224,224))
            
            # convert to grayscale
            img = img.convert('RGB')
            
            # save and overwrite the image
            img.save(image_path)
            print(f"Resizing image: {image_path}")

print("DONE")