import os
import cv2
import numpy as np

from PIL import Image
from PIL.ExifTags import TAGS
from tensorflow import keras
from exif import Image
from subprocess import check_output

def generate_mean_noise_cv2(upload_image_path, dest_dir):

    # Get the base image filename
    im_name = os.path.splitext(os.path.basename(upload_image_path))[0]
    im_extension = os.path.splitext(os.path.basename(upload_image_path))[1]

    # Read the image file
    image = cv2.imread(upload_image_path, cv2.IMREAD_UNCHANGED)

    img_new = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
    img_new = img_new.astype(np.uint8)

    mean_noise_im = 15 * cv2.absdiff(image, img_new)

    mean_noise_fname = im_name + "_mean_noise" + im_extension
    mean_noise_path = os.path.join(dest_dir, mean_noise_fname)
    cv2.imwrite(mean_noise_path, mean_noise_im)

    return mean_noise_im, mean_noise_fname

def estimate_mean_noise_authenticity(mean_noise_im):

    # Resize ELA image
    mean_noise_im = cv2.resize(mean_noise_im, (128, 128), interpolation = cv2.INTER_AREA)
    
    # Fit the resized image to be fed into trained CNN model
    X = np.array(mean_noise_im).flatten() / 255.0
    X = np.array(X)
    X = X.reshape(-1, 128, 128, 3)

    # Load the CNN model
    modelpath = os.path.join("..", "CNN_MODELS", "trained_mean_noise_model.h5")
    model = keras.models.load_model(modelpath)

    # Make prediction
    Y_pred = model.predict(X)

    return Y_pred

def generate_ela_cv2(upload_image_path, dest_dir):

    # Get the base image filename
    im_name = os.path.splitext(os.path.basename(upload_image_path))[0]

    # Read the image file
    im = cv2.imread(upload_image_path, cv2.IMREAD_UNCHANGED)
    
    # Resave the image file with reduced quality
    resave_img_fname = os.path.join(dest_dir, im_name+"_resave_ela.jpeg")
    cv2.imwrite(resave_img_fname, im, [cv2.IMWRITE_JPEG_QUALITY, 90])

    # Read in the saved, reduced quality image file
    resaved_im = cv2.imread(resave_img_fname)

    # Compute ELA
    ela_im = 15 * cv2.absdiff(im, resaved_im)

    # Save the ELA image
    ela_fname = im_name + "_ela_val.jpeg"
    ela_path = os.path.join(dest_dir, ela_fname)
    cv2.imwrite(ela_path, ela_im)

    # Remove the intermediate image
    os.remove(resave_img_fname)

    return ela_im, ela_fname

def estimate_ela_authenticity(ela_im):

    # Resize ELA image
    ela_im = cv2.resize(ela_im, (128, 128), interpolation = cv2.INTER_AREA)
    
    # Fit the resized image to be fed into trained CNN model
    X = np.array(ela_im).flatten() / 255.0
    X = np.array(X)
    X = X.reshape(-1, 128, 128, 3)

    # Load the CNN model
    modelpath = os.path.join("..", "CNN_MODELS", "trained_ela_model.h5")
    model = keras.models.load_model(modelpath)

    # Make prediction
    Y_pred = model.predict(X)

    return Y_pred

def generate_report(upload_image_path, dest_dir, LSB_stego_message, ela_auth, mean_noise_auth):

    ##############################
    # Overall results section
    ##############################

    # Convert fraction to percentage
    ela_auth_true_prob = float('%.2f'%(ela_auth[0][0] * 100))
    ela_auth_false_prob = float('%.2f'%(ela_auth[0][1] * 100))

    # Convert fraction to percentage
    mean_noise_auth_true_prob = float('%.2f'%(mean_noise_auth[0][0] * 100))
    mean_noise_auth_false_prob = float('%.2f'%(mean_noise_auth[0][1] * 100))

    # If we had detected the presence of an encoded message,
    # the image is tampered for sure
    if LSB_stego_message:
        auth_true_prob = 0.00
        auth_false_prob = 100.00
    else:
        auth_true_prob = (ela_auth_true_prob + mean_noise_auth_true_prob) / 2
        auth_false_prob = (ela_auth_false_prob + mean_noise_auth_false_prob) / 2

    if auth_true_prob > 80.00:
        verdict = "Most likely authentic\n"
    elif auth_true_prob > 50.00:
        verdict = "Likely authentic\n"
    elif auth_true_prob > 20.00:
        verdict = "Likely tampered\n"
    else:
        verdict = "Most likely tampered\n"

    final_str = "===========================================\n"
    final_str = final_str + "Overall Image Manipulation Prediction Result:\n"
    final_str = final_str + "===========================================\n\n"

    final_str = final_str + "Overall Authentic probability: " + str(auth_true_prob) + "%\n"
    final_str = final_str + "Overall Tampered probability:  " + str(auth_false_prob) + "%\n\n"

    final_str = final_str + "Verdict:   " + verdict + "\n\n"


    ###########################
    # LSB Stegnography section
    ###########################

    # Initialize a string buffer for building the final report
    final_str = final_str + "===================================\n"
    final_str = final_str + "LSB Stegnography decoder analysis result:\n"
    final_str = final_str + "===================================\n\n"

    # Check if there is any message hidden in the image through stegnography
    if LSB_stego_message:
        final_str = final_str + "-----------------------------------\n"
        final_str = final_str + "Encoded message found:\n"
        final_str = final_str + "-----------------------------------\n\n"
        final_str = final_str + LSB_stego_message + "\n\n"
    else:
        final_str = final_str + "-----------------------------------------------------\n"
        final_str = final_str + "Did not detect any encoded message\n"
        final_str = final_str + "-----------------------------------------------------\n\n"

    ###########################
    # ELA analysis section
    ###########################

    final_str = final_str + "=========================================\n"
    final_str = final_str + "ELA based Authentication Prediction Result:\n"
    final_str = final_str + "=========================================\n\n"

    final_str = final_str + "Authentic probability: " + str(ela_auth_true_prob) + "%\n"
    final_str = final_str + "Tampered probability:  " + str(ela_auth_false_prob) + "%\n\n"


    ##############################
    # Mean noise analysis section
    ##############################

    final_str = final_str + "============================================\n"
    final_str = final_str + "Mean Noise based Authentication Prediction Result:\n"
    final_str = final_str + "============================================\n\n"

    final_str = final_str + "Authentic probability: " + str(mean_noise_auth_true_prob) + "%\n"
    final_str = final_str + "Tampered probability:  " + str(mean_noise_auth_false_prob) + "%\n\n"


    ##############################
    # Image Metadata section
    ##############################

    final_str = final_str + "==============\n"
    final_str = final_str + "Image Metadata:\n"
    final_str = final_str + "==============\n\n"

    metadata_str = str(check_output(["exiftool","-h",upload_image_path]))
    metadata_str = metadata_str.replace("\\n", "")
    metadata_str = metadata_str.replace("\\r", "")
    final_str = final_str + metadata_str[2:-1]


    ##################################
    # Final report writing section
    ##################################

    report_file_name = os.path.splitext(os.path.basename(upload_image_path))[0]
    report_file_name = report_file_name + "_rep.txt"
    report_file_path = os.path.join(dest_dir, report_file_name)

    f = open(report_file_path, "w")
    f.write(final_str)
    f.close()

    return report_file_name
