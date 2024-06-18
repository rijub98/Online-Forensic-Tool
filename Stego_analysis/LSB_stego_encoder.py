import os
import sys
import numpy as np

from PIL import Image

# Get the image filename
image_filepath = sys.argv[1]

# Get the message
message = sys.argv[2]

# Encode the message in a serie of 8-bit values
b_message = ''.join(["{:08b}".format(ord(x)) for x in message ])
b_message = [int(x) for x in b_message]

b_message_length = len(b_message)

# Get the image pixel arrays 
with Image.open(image_filepath) as img:
    width, height = img.size
    data = np.array(img)
    
# Flatten the pixel arrays
data = np.reshape(data, width*height*3)

# Overwrite pixel LSB
data[:b_message_length] = data[:b_message_length] & ~1 | b_message

# Reshape back to an image pixel array
data = np.reshape(data, (height, width, 3))

new_img = Image.fromarray(data)
new_img.save("encoded_image.png")