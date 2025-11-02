import os
import logging 
import sys

logging_str = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
log_dir = "logs"

log_filepath = os.path.join(log_dir,"running_logs.log")

os.makedirs(log_dir,exist_ok=True)