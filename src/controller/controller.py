import queue
import threading
from stream_processing import stream_thread
from my_gui import gui_
from output_handler import save_image
from http_server import http_server
from log_modules import custom_logger
import cv2

with open('cv2_buildInfo.log', 'w', newline='') as file:
    file.write(cv2.getBuildInformation())

# Defining all types of yolo models
PLATE_REGION = 0
PLATE_OCR = 1
CONTAINER_1_CODE = 2
CONTAINER_2_CODE = 3
# Defining gui refresh rate
UPDATE_INTERVAL = 40 #ms

# Responsible for controlling the threads, GUI, transfering data from streams to GUI, storing models
class Controller():
    # Initialize the class with a list of camera names and urls, current version only support 4 cams
    def __init__(self, stream_names: list[str], stream_urls: list[str], max_col: int, folder_path: str) -> None:
        self.logger = custom_logger.get_logger("__Controller__")
        # Folder to save image
        self.folder_path = folder_path
        # Creat event flag for when a truck is present in the lane
        self.truck_detected = threading.Event()
        # Creating a list of camera buffers
        self.cam_buffers = []
        # Create single element queue for each cameras
        for i in range(len(stream_names)):
            self.cam_buffers.append(queue.Queue(maxsize=1))
        self.camera_streams = []
        for i in range(len(stream_names)):
            # Add and start camera streams
            self.camera_streams.append(stream_thread.Stream_thread(stream_names[i], stream_urls[i], self.cam_buffers[i]))
            self.camera_streams[i].start()

        # Storing current frames
        self.current_frames = []

        # Init GUI
        self.app = gui_.App(stream_names, max_col)
        # self.app.bind('<KeyPress>', self.close_gui())
        # Bind http server
        # self.server = http_server.trigger_server(self.app)

        threading.Thread(target=http_server.trigger_server, args=(self.app,)).start()
        self.app.after(UPDATE_INTERVAL, self.update_gui)
        self.app.mainloop()
        # print("Stopping streams...\n")
        for stream in self.camera_streams:
            stream.stop_stream()

    # Schedule tasks to run every UPDATE_INTERVAL, getting data from stream threads and update GUI
    def update_gui(self):
        current_frames = []
        # print("Updating...\n")
        try:
            for buffer in self.cam_buffers:
                labeled_frame = buffer.get(block=False)
                current_frames.append(labeled_frame)
            if len(current_frames) != 0:
                self.app.update_camera_display(current_frames)
        except queue.Empty:
            # logger.warn(f"One or more buffers are empty")
            pass
        
        self.app.after(UPDATE_INTERVAL, self.update_gui)

    def save_images(self):
        for element in self.current_frames:
                save_image.save_classified_image(classified_image=element[0], image_name=element[1], folder_path=self.folder_path)

    def close_gui(self):
        self.app.destroy()