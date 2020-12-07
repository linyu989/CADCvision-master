"""
 @Author       :linyu
 @File         :detection.py
 @Description  :
 @Software     :PyCharm
"""

import cv2 as cv
import numpy as np
import imutils
import matplotlib.pyplot as plt


def plt_show_bgr(imgBGR):
    imgRGB = cv.cvtColor(imgBGR, cv.COLOR_BGR2RGB)
    plt.imshow(imgRGB)
    plt.show()


def detect(cnt):
    shape = "undefined"
    peri = cv.arcLength(cnt, True)
    approx = cv.approxPolyDP(cnt, 0.04 * peri, True)
    if len(approx) == 3:
        shape = "triangle"
    elif len(approx) == 4:
        shape = "rectangle"
    else:
        shape = "circle"

    return shape


def detect_shapes(img, thresh, maxval):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (3, 3), 0)
    ret, thresh = cv.threshold(blurred, thresh, maxval, cv.THRESH_BINARY_INV)
    plt_show_bgr(thresh)
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    output_image = img.copy()
    detections = []
    cX, cY = 0, 0
    for cnt in cnts:
        shape = detect(cnt)
        shape_dict = {"circle": 0, "triangle": 3, "rectangle": 4}
        M = cv.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        detections.append([shape_dict[shape], cY, cX])
        cnt = cnt.astype("int")
        cv.drawContours(output_image, [cnt], -1, (0, 255, 0), 2)
        cv.putText(output_image, f'{shape},({cX},{cY})', (cX, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return output_image, cX, cY


if __name__ == '__main__':
    img = cv.imread('./resource/detection/ball.jpg')
    print(img.dtype)
    output_image, cx, cy = detect_shapes(img, 140, 255)
    print(output_image.shape)
    print(cx, cy)
    print(output_image[cx][cy])
    plt_show_bgr(output_image)
