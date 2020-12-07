"""
 @Author       :linyu
 @File         :feature.py
 @Description  :
 @Software     :PyCharm
"""
# -*- coding: utf-8  -*-
import cv2 as cv
import numpy as np


def feature_detection(img):
    img3 = None
    corners = []
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, (8, 6))
    criteria = (cv.TERM_CRITERIA_MAX_ITER + cv.TERM_CRITERIA_EPS, 30, 0.01)
    corners = cv.cornerSubPix(gray, corners, (3, 3), (-1, -1), criteria)
    if ret:
        corners = np.int0(corners)
        for i in range(len(corners)):
            a, b = corners[i][0][0], corners[i][0][1]
            img3 = cv.circle(img, (a, b), 1, (0, 0, 255), -1)

    return img3, corners


def show():
    imgL = cv.imread('./calibration/capL.jpg')
    imgR = cv.imread('./calibration/capR.jpg')
    print(imgL.dtype)
    hL, wL = imgL.shape[:2]
    print(hL, wL)
    print(imgR.shape[:2])

    detection_imgL, cornersL = feature_detection(imgL)
    detection_imgR, cornersR = feature_detection(imgR)
    cornersR[:, 0, 0] += wL

    cv.imshow("dstL", detection_imgL)
    cv.imshow("dstrR", detection_imgR)
    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()


def dist_checher():
    feature_load = np.load("./detection/feature_coord_detect.npz")
    print(feature_load.files)
    cornersL = feature_load['cornersL']
    cornersR = feature_load['cornersL']

    print(cornersL)
    print(cornersR[:, 0, 0])
    print(cornersR[:, 0, 1])
    print(cornersR[:8, 0, 1])
    print(cornersR[8:16, 0, 1])
    print(cornersR[8:16, 0, 1] - cornersR[:8, 0, 1])

    feature_coord_x = []
    distance_x = []
    distance_y = []

    for i in range(1, 6):
        x = cornersR[i * 8:(i + 1) * 8, 0, 0]
        feature_coord_x.append(x)
        y1 = cornersR[(i - 1) * 8:i * 8, 0, 1]
        y2 = cornersR[i * 8:(i + 1) * 8, 0, 1]
        dist_y = y2 - y1
        distance_y.append(dist_y)

    print(feature_coord_x)
    print(distance_y)
    print(np.mean(distance_y))

    feature_coord_x = np.array(feature_coord_x)
    print(feature_coord_x)

    for i in range(1, 4):
        dist_x = feature_coord_x[:, i + 1] - feature_coord_x[:, i]
        distance_x.append(dist_x)

    print(feature_coord_x[:, 0])
    print(feature_coord_x[:, 2])
    print(distance_x)
    print(np.round(np.mean(distance_x), decimals=2))


if __name__ == '__main__':
    # show()
    feature_load = np.load("./detection/feature_coord_detect.npz")
    print(feature_load.files)

    cornersL = feature_load['cornersL']
    cornersR = feature_load['cornersR']

    print(cornersR)
