import cv2
import os
import numpy as np

def compute_mean_filtered_image_noise_cv2(filename, resize_dim, model_folder_path):

    image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

    img_new = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
    img_new = img_new.astype(np.uint8)

    mean_noise = 15 * cv2.absdiff(image, img_new)

    mean_noise = cv2.resize(mean_noise, resize_dim, interpolation = cv2.INTER_AREA)

    return mean_noise