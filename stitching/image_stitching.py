"""
 @Author       :linyu
 @File         :image_stitching.py
 @Description  :
 @Software     :PyCharm
"""

import cv2 as cv
import imutils
import numpy as np
from imutils import paths
import time
from calibration import calibrator


def image_read(path):
    imagePaths = sorted(list(paths.list_images(path)))
    print(imagePaths)
    images = []
    for imagePath in imagePaths:
        image = cv.imread(imagePath)
        images.append(image)
    return images


def image_stitch(images, crop=True):
    start = time.clock()
    stitcher = cv.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)
    if status == 0:
        if crop:
            stitched = cv.copyMakeBorder(stitched, 2, 2, 2, 2, cv.BORDER_CONSTANT, (0, 0, 0))
            gray = cv.cvtColor(stitched, cv.COLOR_BGR2GRAY)
            thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY)[1]
            contours = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            cnt = max(contours, key=cv.contourArea)
            mask = np.zeros(thresh.shape, dtype="uint8")
            (x, y, w, h) = cv.boundingRect(cnt)
            cv.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
            minRect = mask.copy()
            sub = mask.copy()
            while cv.countNonZero(sub) > 0:
                minRect = cv.erode(minRect, None)
                sub = cv.subtract(minRect, thresh)
            contours = cv.findContours(minRect.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            cnt = max(contours, key=cv.contourArea)
            (x, y, w, h) = cv.boundingRect(cnt)
            stitched = stitched[y:y + h, x:x + w]
        print(f"time taken:{time.clock() - start}")
        return stitched
    else:
        return print(f"image stitching failed {status}")


def video_show():
    camera_data = np.load('./calibration/camera_param_125.npz')
    mtx = camera_data['mtx']
    dist = camera_data['dist']

    capL = cv.VideoCapture(0)
    capR = cv.VideoCapture(1)

    h = int(capL.get(cv.CAP_PROP_FRAME_HEIGHT))
    w = int(capL.get(cv.CAP_PROP_FRAME_WIDTH))
    xLine, YLLeft, YLRight = 248, 355, 625
    radiusL, radiusR = int(30.78), int(29.51)

    while True:
        retL, frameL = capL.read()
        retR, frameR = capR.read()

        frameL = calibrator.undistort(frameL, mtx, dist)
        frameR = calibrator.undistort(frameR, mtx, dist)
        frameL = frameL[0:h, int(0.1 * w):int(0.88 * w)]
        frameR = frameR[0:h, int(0.05 * w):int(0.88 * w)]

        frame_cat = cv.hconcat((frameL, frameR))
        h, w = frame_cat.shape[:2]

        frame_cat[int(xLine - 1):int(xLine + 1), :] = [0, 255, 0]
        frame_cat[:, int(YLLeft - 1):int(YLLeft + 1)] = [0, 255, 0]
        frame_cat[:, int(YLRight - 1):int(YLRight + 1)] = [0, 255, 0]

        cv.circle(frame_cat, (YLLeft, xLine), radiusL, (0, 255, 0))
        cv.circle(frame_cat, (YLRight, xLine), radiusR, (0, 255, 0))

        cv.imshow('capL', frameL)
        cv.imshow('capR', frameR)
        cv.imshow("frame", frame_cat)
        if cv.waitKey(80) & 0xff == 27:
            cv.imwrite("capl_125.jpg", frameL)
            cv.imwrite("capR_125.jpg", frameR)
            cv.destroyAllWindows()
            break
    capL.release()
    capR.release()


def img_show():
    path = './resource/stitchimage'
    images = image_read(path)
    stitched = image_stitch(images, True)
    cv.imshow("Stitched", stitched)
    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()


if __name__ == '__main__':
    # img_show()
    video_show()
