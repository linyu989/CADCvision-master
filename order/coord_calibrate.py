"""
 @Author       :linyu
 @File         :coord_calibrate.py
 @Description  :
 @Software     :PyCharm
"""
# -*- coding: utf-8  -*-
import numpy as np


def get_r_theta(cX, cY, x0, y0, scale_x, scale_y):
    Lx = np.abs(x0 - cX) * scale_x
    Ly = np.abs(y0 - cY) * scale_y
    r = np.sqrt(np.square(Lx) + np.square(Ly))
    theta = 0.0

    if (x0 == cX) and (y0 == cY):
        theta = 0.0

    if (x0 == cX) and (y0 != cY):
        theta = 90.0 if (y0 < cY) else -90.0

    if (y0 == cY) and (x0 != cX):
        theta = 0.0 if (x0 > cX) else 180.0

    if (x0 > cX) and (y0 != cY):
        theta = np.rad2deg(np.arctan(Ly / Lx)) if (y0 < cY) else (-np.rad2deg(np.arctan(Ly / Lx)))

    if (x0 < cX) and (y0 != cY):
        theta = (180 - np.rad2deg(np.arctan(Ly / Lx))) if (y0 < cY) else (-180.0 + np.rad2deg(np.arctan(Ly / Lx)))

    r = np.round(r, decimals=2)
    theta = np.round(theta, decimals=2)
    return r, theta


def pix2world_right(cX, cY, coord_x, coord_y):
    cell = 24.32
    scale_x = cell / 17.87
    scale_y = cell / 18.30
    x0, y0 = coord_x, coord_y
    cX, cY = int(cX), int(cY)
    r, theta = get_r_theta(cX, cY, x0, y0, scale_x, scale_y)

    return r, theta


def pix2world_left(cX, cY, coord_x, coord_y):
    cell = 24.32
    scale_x = cell / 18.60
    scale_y = cell / 18.90
    x0, y0 = coord_x, coord_y
    cX, cY = int(cX), int(cY)
    r, theta = get_r_theta(cX, cY, x0, y0, scale_x, scale_y)

    return r, theta


def camera_choose(cxL, cxR, cY, coord_x, coord_y):
    r, theta = 0.0, 0.0
    if coord_x <= cxL:
        r, theta = pix2world_left(cxL, cY, coord_x, coord_y)
    if coord_x >= cxR:
        r, theta = pix2world_right(cxR, cY, coord_x, coord_y)
    if cxL < coord_x < cxR:
        print("[INFO] Coord Invalid")

    return r, theta


def modulus2rotation(r):
    scale_r = 1000 / 140.25
    rpm = r * scale_r

    return rpm


def theta2rotation(theta):
    scale_r = 500 / 360
    theta_rpm = 0
    theta_rpm = (theta * scale_r) if theta >= 0 else (-((360.0 + theta) * scale_r))

    return theta_rpm


def modulusAndtheta2rpm(r, theta):
    r0 = 30.88
    rpm = 3000
    if r < r0:
        print("[INFO] Invalid Area")
        rpm = rpm
    else:
        rpm = rpm - modulus2rotation(r - r0)
    theta0 = 90.00
    theta = 0 if (theta == 0) and (r == 0) else theta0 - theta
    theta_rpm = theta2rotation(theta)
    rpm = np.round(rpm, decimals=2)
    theta_rpm = np.round(theta_rpm, decimals=2)

    return rpm, theta_rpm


def coord2rotation_change(YLLeft, YLRight, xLine, coord_x, coord_y):
    r, theta = camera_choose(YLLeft, YLRight, xLine, coord_x, coord_y)
    r_rpm, theta_rpm = modulusAndtheta2rpm(r, theta)
    r_rpm = 930 if r_rpm < 930 else r_rpm
    r_rpm, theta_rpm = int(np.round(r_rpm, decimals=0)), int(np.round(theta_rpm, decimals=0))

    return r_rpm, theta_rpm


if __name__ == '__main__':
    xLine, YLLeft, YLRight = 248, 355, 625
    coord_x, coord_y = 56, 40
    r, theta = camera_choose(YLLeft, YLRight, xLine, coord_x, coord_y)
    print(r, theta)
    r_rpm, theta_rpm = modulusAndtheta2rpm(r, theta)
    print(r_rpm, theta_rpm)
    print(theta2rotation(72))
    rpm01, thetapm01 = coord2rotation_change(YLLeft, YLRight, xLine, coord_x, coord_y)
    print(rpm01, thetapm01)
