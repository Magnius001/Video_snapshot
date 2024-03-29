import os
import customtkinter
import cv2
from PIL import Image
from output_handler import save_image
from log_modules import custom_logger

# Get screen resolution
import ctypes
user32 = ctypes.windll.user32
# Get screen size
# 0 -> width
# 1 -> height
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# Setup customtkinter theme
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Define colors
BACK_GROUND_COLOR = '#2c2f33'
# ACCENT_COLOR = '#7289da'
# ACCENT_COLOR = '#12ee64'
ACCENT_COLOR = '#0ad355'
GREEN_STATUS_COLOR = '#58e91d'
RED_STATUS_COLOR = '#f44336'
WHITE_COLOR = '#ffffff'

#Status display clear interval (frames)
STATUS_CLEAR_INTERVAL = 150

gui_logger = custom_logger.get_logger("__GUI__")

# Main app
class App(customtkinter.CTk):
    def __init__(self, camera_types : list[str], max_col : int):
        super().__init__()
        # Configure window
        self.title("Portlogics")
        self.geometry(f"{screensize[0]}x{screensize[1]}")
        # Start in fullscreen
        # self.attributes('-fullscreen', True)
        self.state('zoomed')
        self.config(padx=5, pady=5)

        # Configure grid layout 2x3
        self.columnconfigure(0, weight=4)
        # self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=2, minsize=int(screensize[1]*0.08))

        # Set grid dimension for view frame
        self.max_col = max_col
        self.max_row = len(camera_types)//max_col + (len(camera_types)%max_col > 0)

        # Create view frame
        self.view_frame = customtkinter.CTkFrame(self, fg_color=BACK_GROUND_COLOR, corner_radius=4)
        self.view_frame.grid(row=0, column=0, columnspan=1, rowspan=1, pady=5, padx=5, sticky="new")
        for i in range(self.max_row):
            self.view_frame.rowconfigure(i, weight=1)
        for i in range(self.max_col):
            self.view_frame.columnconfigure(i, weight=1)

        # Create control frame
        self.control_frame = customtkinter.CTkFrame(self, fg_color=BACK_GROUND_COLOR, corner_radius=4)
        self.control_frame.grid(row=1, column=0, columnspan=1, rowspan=1, pady=5, padx=5, sticky="nsew")
        for i in range(2):
            self.control_frame.columnconfigure(i, weight=1)
        self.control_frame.rowconfigure(0, weight=1)


        # Dimensions for each camera
        self.camera_width = int(float(screensize[0])/float(max_col))
        # camera_width = 740
        self.camera_height = int(float(screensize[1]*0.8)/float(self.max_row))
        # self.camera_height = self.camera_width*9/16
        # camera_height = 480

        # Adding camera displays
        self.cameras = []
        for i in range(self.max_row*max_col):
            self.cameras.append(list())
        row = 0
        col = 0
        counter = 1
        for camera, camera_type in zip(self.cameras, camera_types):
            camera.append(customtkinter.CTkFrame(self.view_frame))
            camera.append(customtkinter.CTkLabel(camera[0]))
            camera.append(customtkinter.CTkLabel(camera[1]))
            self._setup_camera_display(camera, row, col, f" {camera_type.capitalize()}")

            if counter != 0 and counter % self.max_col == 0:
                col = 0
                row += 1
            else:
                col += 1

            counter += 1

        #Adding buttons
        # self.button = []
        self.button = customtkinter.CTkButton(self.control_frame, text='CAPTURE', width=self.camera_width, bg_color='transparent', fg_color='red', corner_radius=30, hover_color=ACCENT_COLOR, text_color=WHITE_COLOR, font=customtkinter.CTkFont(size=30, weight="bold"), command=self.save_images)
        self.button.grid(row=0, column=1, padx=5, pady=5, sticky='ns')

        # status window
        self.status_display = customtkinter.CTkLabel(self.control_frame, width=self.camera_width, text=' ', anchor='nw', justify='left', font=customtkinter.CTkFont(size=15, weight="bold"))
        self.status_display.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        # Storing current images
        self.images = []

        # 
        self.status_counter = 0

        # Save folder path
        self.folder_path = 'saved_images'
                
        
    def _setup_camera_display(self, _display:list, row:int, col:int, camera_type: str):
        # WidgetFrame
        _display[0].configure(width=450, fg_color=BACK_GROUND_COLOR, border_color=ACCENT_COLOR, border_width=2, corner_radius=0)
        _display[0].grid(row=row, column=col, pady=5, padx=5)
        _display[0].rowconfigure(0, weight=1)
        _display[0].columnconfigure(0, weight=1)

        # Label which has the camera image
        _display[1].configure(width=self.camera_width, height=self.camera_height, text='', bg_color= 'transparent', anchor='s')
        _display[1].grid(row=0, column=0, padx=5, pady=5, sticky="n")

        # Label to store the camera name
        _display[2].configure(text=camera_type, text_color=WHITE_COLOR, bg_color= ACCENT_COLOR, corner_radius=0, font=customtkinter.CTkFont(size=18, weight="bold"))
        _display[2].place(relx=1, rely=1, x=0, y=1,anchor="se")
    
    def update_camera_display(self, images: list[tuple]):
        self.images=images
        try:
            for camera, im in zip(self.cameras, images):
                im = im[0]
                # Convert BGR to RGB
                blue,green,red = cv2.split(im)
                im = cv2.merge((red,green,blue))
                im = Image.fromarray(im)
                # Add image to GUI
                imtk = customtkinter.CTkImage(dark_image=im, size=(self.camera_width, self.camera_height-5))
                camera[1].configure(image = imtk)
                camera[1].image = imtk
        except Exception as e:
            gui_logger.error(f"In update cam display: {e}")
        if self.status_counter >= STATUS_CLEAR_INTERVAL:
            # Clear status display after certain number of GUI refresh cycles
            self.clear_status_display()
            self.status_counter = 0
        self.status_counter += 1

    def update_status(self, file_paths: list[str]):
        if file_paths is None:
            # Error saving
            output = "Unable to save images."
            gui_logger.warn(output)
            status_color = RED_STATUS_COLOR
        else:
            output = f"Sucessfully saved {len(file_paths)} images."
            gui_logger.info(output)
            # for file_path in file_paths:
            #     output += f"\n    {file_path}"
            status_color = GREEN_STATUS_COLOR
        self.status_display.configure(text=output, text_color=status_color)
        # self.status_display.after(1000, self.clear_status_display())

    def clear_status_display(self):
        self.status_display.configure(text='')

    def save_images(self, container_details: str = None):
        folder_path = self.folder_path
        if container_details is not None:
            folder_path =  os.path.join(folder_path, container_details)
            print(f"Saved in: {self.folder_path}\n")
        self.update_status(save_image.save_classified_images(self.images, self.folder_path, container_details))


def test(new_app : App):
    images = []
    for i in range(20):
        images.append(cv2.imread(r"E:\Internship\Common_resources\official_train_img\images\images\1.png"))
    # images.append(cv2.imread(r"E:\Internship\Common_resources\Screenshots\cam_20070_c.png"))
    # images.append(cv2.imread(r"E:\Internship\Common_resources\Screenshots\cam_20075_c.png"))
    # images.append(cv2.imread(r"E:\Internship\Common_resources\Screenshots\cam_20078_c.png"))
    # images.append(cv2.imread(r"E:\Internship\Common_resources\Screenshots\cam_20079_c.png"))

    new_app.update_camera_display(images=images)
    new_app.mainloop()