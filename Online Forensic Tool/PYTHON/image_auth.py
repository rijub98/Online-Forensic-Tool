#! C:/Users/ri332/AppData/Local/Programs/Python/Python310/python.exe

import sys
import os

from image_auth_helper import generate_ela_cv2
from image_auth_helper import estimate_ela_authenticity
from image_auth_helper import generate_mean_noise_cv2
from image_auth_helper import estimate_mean_noise_authenticity
from image_auth_helper import generate_report
from image_stego_helper import LSB_stego_decode

# Get the filename from the command argument
filename = sys.argv[1]

src_dir = os.path.join("..", "UPLOADS", "IMAGES")
src_file_path = os.path.join(src_dir, filename)

# Check if there is any text message hidden in the LSBs
LSB_stego_message = LSB_stego_decode(src_file_path)

dest_dir = os.path.join("..", "RESULTS", "IMAGES")
ela_im, ela_filename = generate_ela_cv2(src_file_path, dest_dir)

# Check if image is authentic as per its ELA
ela_auth = estimate_ela_authenticity(ela_im)

mean_noise_im, mean_noise_filename = generate_mean_noise_cv2(src_file_path, dest_dir)

# Check if image is authentic as per its mean noise
mean_noise_auth = estimate_mean_noise_authenticity(mean_noise_im)

report_file_name = generate_report(src_file_path, dest_dir, LSB_stego_message, ela_auth, mean_noise_auth)

to_print = report_file_name + "\n" + ela_filename + "\n" + mean_noise_filename + "\n"
print(to_print)