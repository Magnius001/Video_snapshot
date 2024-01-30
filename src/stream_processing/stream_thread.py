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
        cam = cv2.VideoCapture(self.stream_url, cv2.CAP_ANY)
        # cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        print(f"Stream resolution: {cam.get(cv2.CAP_PROP_FRAME_WIDTH)} x {cam.get(cv2.CAP_PROP_FRAME_HEIGHT)} - {cam.getBackendName()}\n")
        if cam.isOpened():
            rval, frame = cam.read()
        else:
            rval = False

        while True:
            try:
                if rval:
                    # frame = cv2.resize(frame, (640, 640))
                    self.buffer.put((frame,self.stream_name), block=False)
            except:
                pass
            cv2.waitKey(1)
            rval, frame = cam.read()
            if self.stop_flag:
                break
        cam.release()
        os._exit(1)

    def stop_stream(self):
        self.stop_flag = True
