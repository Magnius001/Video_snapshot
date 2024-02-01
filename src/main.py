import configparser
from controller import controller

def main():
    camera_names = []
    camera_urls = []

    # Reading in config
    config = configparser.ConfigParser()
    config.read('config.ini')
    # Getting cameras names and their respetive urls
    for camera in config['CAMERA'].items():
        camera_names.append(camera[0])
        camera_urls.append(camera[1])
    
    #Getting number of columns
    max_col = int(config['SPECIFICATION']['Col'])
            
    new_controller = controller.Controller(camera_names, camera_urls, max_col, r"src\saved_images")

if __name__ == "__main__":
    main()