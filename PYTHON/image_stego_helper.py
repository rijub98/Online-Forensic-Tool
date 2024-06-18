import os
import cv2
import numpy as np

from PIL import Image

def LSB_stego_decode(image_filepath):

    image = Image.open(image_filepath)

    binary_data = np.array(image)
    height, width, colors = binary_data.shape

    # Flatten the image pixels
    binary_data = np.reshape(binary_data, width*height*colors)
    
    # extract LSB
    binary_data = binary_data & 1
    
    # Packs binary-valued array into 8-bits array.
    binary_data = np.packbits(binary_data)

    # convert from bits to characters
    decoded_data = ""
    for byte in binary_data:

        ch = chr(byte)

        # If it is a valid character, record it
        if (ch >= chr(32)) and (ch <= chr(126)):
            decoded_data = decoded_data + ch

        # Special characters like '\t' and '\n' are ignored
        # break for anything else
        elif (ch != chr(9)) and (ch != chr(13)):
            break

    return decoded_data