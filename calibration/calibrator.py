"""
 @Author       :linyu
 @File         :calibrateClass.py
 @Description  :
 @Software     :PyCharm
"""

import cv2 as cv
import numpy as np
import glob
from imutils import paths


class cameraClibration():
    def __init__(self, path):
        self.criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = np.zeros((6 * 8, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)
        self.objpoints = []
        self.imgpoints = []
        self.path = path
        self.imgSize = None

    def calibrate(self):
        images = paths.list_images(self.path)
        for frame in images:
            print(frame)
            img = cv.imread(frame)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            self.imgSize = gray.shape[::-1]
            ret, corners = cv.findChessboardCorners(gray, (8, 6))
            if ret:
                self.objpoints.append(self.objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                self.imgpoints.append(corners2)
        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv.calibrateCamera(self.objpoints, self.imgpoints,
                                                                                   self.imgSize, None, None)
        print(self.mtx, "\n")
        print(self.dist, "\n")
        np.savez('./calibration/camera_param', ret=self.ret, mtx=self.mtx, dist=self.dist, rvecs=self.rvecs,
                 tvecs=self.tvecs)
        return self.mtx, self.dist


def undistort(img1, mtx, dist):
    h, w = img1.shape[:2]
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0)
    dst = cv.undistort(img1, mtx, dist, None, newCameraMatrix)

    return dst


if __name__ == '__main__':

    camera_data = np.load('./calibration/camera_param_120.npz')
    print(camera_data.files)
    mtx = camera_data['mtx']
    dist = camera_data['dist']
    print(mtx)
    print(dist)
    img1 = cv.imread("./calibration/checkerboard/WIN_20201010_15_14_38_Pro.jpg")
    dst = undistort(img1, mtx, dist)
    cv.namedWindow("undistort", cv.WINDOW_AUTOSIZE)
    cv.imshow("undistort", dst)
    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()
