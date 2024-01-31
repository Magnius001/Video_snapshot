# import atexit
# import json
# import queue
# import logging.config
# import logging.handlers
# import pathlib
# import os

# logger = logging.getLogger("__my_logger__")  # __name__ is a common choice

# # LOGGING
# LOG_DIR = 'log'
# LOG_FILE = '/log.json'
# LOG_PATH = LOG_DIR + LOG_FILE

# if not os.path.exists(LOG_DIR):
#     os.mkdir(LOG_DIR)

# if not os.path.exists(LOG_PATH):
#     f = open(LOG_PATH, 'a').close() #create empty log file
# else:
#     f = open(LOG_PATH,"w").close() #clear log file


# def setup_logging() -> None:
#     config_file = pathlib.Path("logging_config.json")
#     with open(config_file) as file_in:
#         config = json.load(file_in)

#     logging.config.dictConfig(config)
#     queue_handler = logging.getHandlerByName("queue_handler")
#     if queue_handler is not None:
#         queue_handler.listener.start()
#         atexit.register(queue_handler.listener.stop)

# # def main():
# #     setup_logging()
# #     logging.basicConfig(level="INFO")
# #     logger.debug("debug message", extra={"x": "hello"})
# #     logger.info("info message")
# #     logger.warning("warning message")
# #     logger.error("error message")
# #     logger.critical("critical message")
# #     try:
# #         1 / 0
# #     except ZeroDivisionError:
# #         logger.exception("exception message")

# # if __name__ == "__main__":
# #     main()

import logging
import sys
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "app_log.log"

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler
def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger