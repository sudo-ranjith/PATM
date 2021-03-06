from datetime import datetime
import traceback
from flask import jsonify
from time import time
# Read an image from a directory "input"
# fetch a particular region of text in the image
# and write the text in a file "output"
import os
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
import sys
import json


input_dir = "/home/sudo-ranjith/Documents/predominentex/input/Bharath Agencies"
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_file = "output.txt"

def get_image_text(image_path, img_config):
    func_resp = {}
    res_data = []
    print(f"image_path : {image_path}")
    try:
        # read image
        img = cv2.imread(image_path)

        # fetch text from image from the given region X1, Y1, X2, Y2
        # X1, Y1, X2, Y2 are the coordinates of the region
        # X1, Y1 are the top left corner
        # X2, Y2 are the bottom right corner

        for points_dict in img_config:
            one_data = {}
            x1, y1, x2, y2 = int(points_dict["xMin"]), int(points_dict["yMin"]), int(points_dict["xMax"]), int(points_dict["yMax"])
            roi = img[y1:y2, x1:x2]
            # write the text in a file
            with open(os.path.join(output_dir, output_file), "a") as f:
                f.write(f"{points_dict['name']}" + pytesseract.image_to_string(roi, lang='eng') + "\n")
            one_data[points_dict['name']] = pytesseract.image_to_string(roi, lang='eng').strip()
            res_data.append(one_data)
    except Exception as e:
        func_resp["message"] = traceback.format_exc()
        func_resp["status"] = "failure"
    finally:
        func_resp["data"] = res_data
        return func_resp


# REF: https://www.geeksforgeeks.org/decorators-in-python/
def calculate_proc_time(job):
    def _wrap(*args, **kwargs):
        proc_start = time()
        func_resp = job(*args, **kwargs)
        proc_end = time()
        func_resp["time_stamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        func_resp["run_time"] = f"{proc_end - proc_start:.2f} seconds"
        return jsonify(func_resp)
    return _wrap
