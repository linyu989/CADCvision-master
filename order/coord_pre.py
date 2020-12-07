"""
 @Author       :linyu
 @File         :coord_pre.py
 @Description  :
 @Software     :PyCharm
"""
# -*- coding: utf-8  -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error


def pre_coord():
    M_cam = np.array([[809, 1080], [532, 1044], [1113, 911], [328, 897], [884, 788],
                      [400, 600], [756, 552], [412, 384], [973, 334], [619, 241]], dtype="float32")
    Origin_robot = np.array([455.68, -165.10])
    M_rob = np.array([[623.47, -0.95], [617.58, -45.52], [596.12, 46.09], [594.37, -78.05],
                      [576.27, 11.15], [546.80, -65.44], [539.73, -9.13], [512.83, -64.04],
                      [505.32, 24.31], [490.97, -31.61]], dtype="float32") - Origin_robot
    A = np.linalg.inv(M_cam.T.dot(M_cam)).dot(M_cam.T).dot(M_rob)
    M_pred = M_cam.dot(A)
    mean = np.sqrt((M_pred - M_rob) ** 2).mean()
    meanX = np.sqrt((M_pred[:, 0] - M_rob[:, 0]) ** 2).mean()
    meanY = np.sqrt((M_pred[:, 1] - M_rob[:, 1]) ** 2).mean()
    clf = linear_model.Ridge()
    clf.fit(M_cam[:8], M_rob[:8])
    M_pred_ridge = clf.predict(M_cam)
    squared_error = mean_squared_error(M_pred_ridge, M_rob)
    squared_errorX = mean_squared_error(M_pred_ridge[:, 0], M_rob[:, 0])
    squared_errorY = mean_squared_error(M_pred_ridge[:, 1], M_rob[:, 1])
    predict = clf.predict(M_cam[8:])

    return predict


if __name__ == '__main__':
    coord = pre_coord()
    print(coord)
