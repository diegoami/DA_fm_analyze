import cv2
import pytesseract
from PIL import Image
from os.path import basename
import numpy as np
target_text = "GK,DR,DCR,DCL,DL,MCR,MCL,AMR,AC,AML,STC,S1,S2,S3,S4,S5,S6,S7"
distance_map= {}
import Levenshtein
def convert_image_dpi(image_path, dpi):
    img = Image.open(image_path)
    img_300dpi = img.convert("L").resize(img.size, Image.ANTIALIAS)
    img_300dpi.save("temp_image_300dpi.png", dpi=(dpi, dpi))
    return "temp_image_300dpi.png"


def process_image(image_path):
    image_300dpi_path = convert_image_dpi(image_path, 300)
    image = cv2.imread(image_300dpi_path)
    cv2.imwrite(basename(image_path) + ".png", image)

    return image

def process_image_gray(image_path, block_size=15, c=5, blur=3):
    image = process_image(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.bitwise_not(image)

    #_, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Apply adaptive thresholding to highlight the text
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size , c)
    image = cv2.medianBlur(image, blur)

    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    #image = cv2.erode(image, kernel, iterations=1)
   # image = cv2.dilate(image, kernel, iterations=1)

    cv2.imwrite(f"{basename(image_path)}_{block_size}_{c}.png", image)
    return image


# Load the image
def read_image(image_path, process_method, custom_config):
    if process_method == process_image_gray:
        #for block_size in [3,5,7,9,11,13,15]:
        #    for c in [2,5,8,10,13,16]:
        #         for blur in [3,5,7,9,11,13,15]:
        for block_size in [9]:
            for c in [5]:
                blur = 5
                print(f"block_size: {block_size}, c: {c}, blur: {blur}")
                image = process_method(image_path, block_size=block_size, c=c)
                text = pytesseract.image_to_string(image, config=custom_config)
                text_line =",".join(text.splitlines())
                distance = Levenshtein.distance(text_line, target_text)
                print(text_line)
                print(distance)
    else:
        image = process_method(image_path)
        text = pytesseract.image_to_string(image, config=custom_config)
    return text


#d2_text = read_image(image_path="/Users/diego/projects/ocr-with-tesseract/images/d2.JPG", process_method=process_image,
#                      custom_config=r"--psm 6 -c tessedit_char_whitelist=0123456789 -c load_system_dawg=0 -c load_freq_dawg=0")

d1_text = read_image(image_path="/Users/diego/projects/ocr-with-tesseract/images/d1.JPG", process_method=process_image_gray,
                      custom_config=r"--psm 6  -c tessedit_char_whitelist=GKDCRLMSTA1234567 -c load_system_dawg=0 -c load_freq_dawg=0")


#print(d2_text)
#print(d1_text)