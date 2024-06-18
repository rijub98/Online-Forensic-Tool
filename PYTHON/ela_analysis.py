import os
import cv2
import PIL
from PIL import Image, ImageChops, ImageEnhance

def ela_cv2(fname, quality, resize_dim, model_folder_path):

    resave_img_fname = os.path.join(model_folder_path,"resave_ela.jpeg")
    scale = 15
    im = cv2.imread(fname, cv2.IMREAD_UNCHANGED)
    cv2.imwrite(resave_img_fname, im, [cv2.IMWRITE_JPEG_QUALITY, quality])

    resaved_im = cv2.imread(resave_img_fname)
    diff1 = scale * cv2.absdiff(im, resaved_im)

    ela_im = cv2.resize(diff1, resize_dim, interpolation = cv2.INTER_AREA)

    os.remove(resave_img_fname)
    return ela_im
