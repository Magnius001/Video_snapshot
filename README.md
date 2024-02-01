# VIDEO CAPTURE USING HTTP TRIGGER
## Status: Ended
This project take video streams and save selected images based on HTTP POST request

Plan for improvements:
- Sync all camera.
- Reduce lag to real-time.
- Implement multiprocessing to support more camera feeds
## How to run
### Installing libraries
All required modules have been listed in the requirements.txt folder in root directory.
To install them with pip:
```
pip install -r requirements.txt
```
In case that does not work, here is how to install the libraries manually.
#### OpenCV, Pandas and CustomTkinter
They can be install by running the following code:
```
pip install opencv-python
pip install pandas
pip install customtkinter
```
### Config file
Camera names, urls and layout are define in the bundled `config.ini` file.
### Running the application
To run the application, we only need to execute the main.py script in the src folder. The command is as follow:
```
python -u src\main.py
```
