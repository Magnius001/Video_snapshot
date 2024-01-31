# Define class for the camera thread.
import os
import queue
import threading
import cv2
import time
from log_modules import custom_logger

class Stream_thread(threading.Thread):

    def __init__(self, stream_name, stream_url, buffer: queue.Queue[tuple]):
        threading.Thread.__init__(self)
        self.stream_name = stream_name
        self.stream_url = stream_url
        self.buffer = buffer
        self.stop_flag = False
        self.logger = custom_logger.get_logger(f"__Stream{stream_name}__")

    def run(self):
        self.logger.info(f"Starting {self.stream_name}")
        self.launch_stream()

    def launch_stream(self):
        cam = cv2.VideoCapture(self.stream_url, cv2.CAP_ANY)
        cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.logger.info(f"Stream resolution: {cam.get(cv2.CAP_PROP_FRAME_WIDTH)} x {cam.get(cv2.CAP_PROP_FRAME_HEIGHT)}\n")
        if cam.isOpened():
            rval, frame = cam.read()
        else:
            rval = False

        while True:
            try:
                if rval:
                    # frame = cv2.resize(frame, (640, 640))
                    self.buffer.put((frame,self.stream_name), block=False)
                else:
                    self.logger.warn("Unable to get frame")
                    break
            except:
                pass
            cv2.waitKey(1)
            rval, frame = cam.read()
            if self.stop_flag:
                # os._exit(1)
                break
        
        cam.release()
        # Attemp to relaunch stream
        if not self.stop_flag:
            time.sleep(1)
            self.logger.warn("Lost connection, attempting to restart stream")
            self.launch_stream()
        else:
            os._exit(1)

    def stop_stream(self):
        self.logger.info(f"Stopping stream thread {self.stream_name}")
        self.stop_flag = True
