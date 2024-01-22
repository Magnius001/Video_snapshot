# Define class for the camera thread.
import os
import queue
import threading
import cv2

class Stream_thread(threading.Thread):

    def __init__(self, stream_name, stream_url, buffer: queue.Queue[tuple]):
        threading.Thread.__init__(self)
        self.stream_name = stream_name
        self.stream_url = stream_url
        self.buffer = buffer
        self.stop_flag = False

    def run(self):
        # print("Starting " + self.stream_name)
        self.launch_stream()

    def launch_stream(self):
        cam = cv2.VideoCapture(self.stream_url)
        if cam.isOpened():
            rval, frame = cam.read()
        else:
            rval = False

        while rval:
            try:
                self.buffer.put((frame,self.stream_name), block=False)
            except:
                pass
            cv2.waitKey(5)
            rval, frame = cam.read()
            if self.stop_flag or not rval:
                break
        cam.release()
        os._exit(1)

    def stop_stream(self):
        self.stop_flag = True
