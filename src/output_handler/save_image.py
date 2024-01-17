import os
import pathlib
import time
import cv2
import numpy
from datetime import datetime

def save_classified_images(classified_images: list[tuple], folder_path:str) -> bool:
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
    # print(type(classified_images))
    for element in classified_images:
        file_path = os.path.join(folder_path, f"{element[1]}_{round(time.time() * 1000)}.jpg")
        flag = cv2.imwrite(file_path, element[0])
        # print(flag, '\n')
        return flag
    
def save_one_image(classified_image: numpy.ndarray, folder_path:str) -> bool:
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
    # print(type(classified_images))
    file_path = os.path.join(folder_path, f"{round(time.time() * 1000)}.jpg")
    flag = cv2.imwrite(file_path, classified_image)
    # print(flag, '\n')
    return flag

def save_classified_image(classified_image: numpy.ndarray, image_name: str, folder_path:str) -> str:
    folder_path =  os.path.join(folder_path, f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S_%f')}")
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
    # print(type(classified_images))
    file_path = os.path.join(folder_path, f"{image_name}.jpg")
    # flag = cv2.imwrite(file_path, classified_image)
    if cv2.imwrite(file_path, classified_image):
        return file_path
    return None
