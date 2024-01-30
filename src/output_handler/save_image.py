import os
import pathlib
import time
import cv2
import numpy
from datetime import datetime

def save_classified_images(classified_images: list[tuple], folder_path:str, details:str = None) -> list[str]:
    folder_path =  os.path.join(folder_path, f"{datetime.now().strftime('%y%m%d%H%M%S')}_{details}")
    print(f"Saved in: {folder_path}\n")
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
    # print(type(classified_images))
    saved_file_paths = []
    for element in classified_images:
        file_path = os.path.join(folder_path, f"{element[1]}.jpg")
        if not cv2.imwrite(file_path, cv2.resize(element[0], (640, 640)), [cv2.IMWRITE_JPEG_QUALITY, 50]):
            return None
        saved_file_paths.append(file_path)
    return saved_file_paths
    
def save_one_image(classified_image: numpy.ndarray, folder_path:str) -> bool:
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
    # print(type(classified_images))
    file_path = os.path.join(folder_path, f"{round(time.time() * 1000)}.jpg")
    flag = cv2.imwrite(file_path, classified_image)
    # print(flag, '\n')
    return flag

def save_classified_image(classified_image: numpy.ndarray, image_name: str, folder_path:str) -> str:
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(folder_path, f"{image_name}.jpg")
    if cv2.imwrite(file_path, classified_image):
        return file_path
    return None
