import os
import sys
from controller import controller
from my_gui import gui_

# # Defining all types of yolo models
# PLATE_REGION = 0
# PLATE_OCR = 1

def main():
    # for thread in support_threads:
    #     thread.start()
    camera_types = ['FRONT', 'BACK', 'CON1', 'CON2']
    stream_urls = []
    # # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.111:554/media/video2&172.16.17.111:80/LAPI/V1.0/Channels/1")
    # # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.112:554/media/video2&172.16.17.112:80/LAPI/V1.0/Channels/1")
    # # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1")
    # # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1")
    # stream_urls.append(r"E:\Internship\ML_simplePython_2\ML_simplePython\test_video\x2mate.com-SmartGate.mp4")
    # stream_urls.append(r"E:\Internship\ML_simplePython_2\ML_simplePython\test_video\x2mate.com-SmartGate.mp4")
    # stream_urls.append(r"E:\Internship\ML_simplePython_2\ML_simplePython\test_video\x2mate.com-SmartGate.mp4")
    # stream_urls.append(r"E:\Internship\ML_simplePython_2\ML_simplePython\test_video\x2mate.com-SmartGate.mp4")
    # new_app = controller.Controller(stream_names, stream_urls)
    
    stream_names = []
    for i in range(1):
        for camera_type in camera_types:
            stream_names.append(f'{camera_type}-{i}')
            stream_urls.append(r"E:\Internship\ML_simplePython_2\ML_simplePython\test_video\x2mate.com-SmartGate.mp4")
            
    # new_app = gui_.App(['FRONT', 'BACK', 'CON1', 'CON2'], 1)
    new_controller = controller.Controller(stream_names, stream_urls, r"src\saved_images")
    
    # print("Exiting...\n")
    # os._exit(1)

if __name__ == "__main__":
    main()