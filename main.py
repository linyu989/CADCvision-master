"""
 @Author       :linyu
 @File         :main.py
 @Description  :
 @Software     :PyCharm
"""
# -*- coding: utf-8  -*-
import numpy as np
import cv2 as cv
import cvui
import argparse
import imutils
import time
import math
from order import coord_calibrate
from calibration import calibrator
from communication import com_engine
from stitching import image_stitching
from detection import shape_detect
from order import order_master

ap = argparse.ArgumentParser()
ap.add_argument("-vL", "--videoL", required=True, help="path to videoL file")
ap.add_argument("-vR", "--videoR", required=True, help="path to videoR file")
ap.add_argument("-COM", "--ComPort", required=True, help="path to COM-Port")
args = vars(ap.parse_args())

pathL = args['videoL']
pathR = args['videoR']

if (len(pathL) == 1) and ('0' <= pathL <= '9'): pathL = int(pathL)
if (len(pathR) == 1) and ('0' <= pathR <= '9'): pathR = int(pathR)

coord_x_list, coord_y_list = [0], [0]
main_ui = "mainui"
win_name_cvui = "cvui"
data = "undefined"
object_dict = {'r': 0.0, 'theta': 0.0, 'object': 'N', 'action': 'N'}

serial_communication = com_engine.SerialCommunication(args['ComPort'], 9600, 0.5)
serial_communication.open_engine()

camera_data = np.load('calibration/camera_param_125.npz')
mtx = camera_data['mtx']
dist = camera_data['dist']


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        if (x != coord_x_list[-1]) and (y != coord_y_list[-1]):
            coord_x_list.append(x)
            coord_y_list.append(y)
        cv.circle(frame_cat, (x, y), 1, (0, 0, 255), thickness=-1)
        cv.putText(frame_cat, xy, (x, y), cv.FONT_HERSHEY_PLAIN,
                   1.0, (0, 0, 0), thickness=1)
        cv.imshow(main_ui, frame_cat)
    return coord_x_list, coord_y_list


capL = cv.VideoCapture(pathL)
capR = cv.VideoCapture(pathR)

cvui.init(win_name_cvui)
frame_height = int(capL.get(cv.CAP_PROP_FRAME_HEIGHT))
frame_width = int(capL.get(cv.CAP_PROP_FRAME_WIDTH))

cvui_img = np.zeros((frame_height, 200, 3), np.uint8)
cvui_img[:] = [0x21, 0x21, 0x21]

start_col = int(frame_width * 0.1)
start_row = int(frame_height * 0.1)
button_width = 70
button_height = 40
xLine, YLLeft, YLRight = 248, 355, 625
radiusL, radiusR = int(40.50), int(41.78)
start_X, start_Y = 0, 110

while True:
    ret, frameL = capL.read()
    retR, frameR = capR.read()

    frameL = calibrator.undistort(frameL, mtx, dist)
    frameR = calibrator.undistort(frameR, mtx, dist)

    frameL = frameL[0:frame_height, int(0.1 * frame_width):int(0.88 * frame_width)]
    frameR = frameR[0:frame_height, int(0.05 * frame_width):int(0.88 * frame_width)]

    frame_cat = cv.hconcat((frameL, frameR))
    frame_height, frame_width = frame_cat.shape[:2]

    frame_cat[int(xLine - 1):int(xLine + 1), :] = [0, 255, 0]
    frame_cat[:, int(YLLeft - 1):int(YLLeft + 1)] = [0, 255, 0]
    frame_cat[:, int(YLRight - 1):int(YLRight + 1)] = [0, 255, 0]

    cv.circle(frame_cat, (YLLeft, xLine), radiusL, (0, 255, 0))
    cv.circle(frame_cat, (YLRight, xLine), radiusR, (0, 255, 0))
    cv.circle(frame_cat, (YLLeft, xLine), 240, (0, 255, 0))

    if (cvui.button(cvui_img, start_col, start_row, button_width, button_height, "Ball")):
        object_dict['object'] = 'q'
        print("Ball clicked")

    if (cvui.button(cvui_img, start_col, start_row + 50, button_width, button_height, "Cube")):
        object_dict['object'] = 'm'
        print("Cube clicked")

    if (cvui.button(cvui_img, start_col, start_row + 100, button_width, button_height, "Up")):
        object_dict['action'] = 'z'
        print("Up clicked")

    if (cvui.button(cvui_img, start_col, start_row + 150, button_width, button_height, "Down")):
        object_dict['action'] = 'f'
        print("Down clicked")

    if (cvui.button(cvui_img, start_col, start_row + 250, button_width, button_height, "Send")):
        print("Send clicked")
        print(frame_height, frame_width)
        print(f"x0,y0 : {coord_x_list[-1], coord_y_list[-1]}")

        r_rpm, theta_rpm = coord_calibrate.coord2rotation_change(YLLeft, YLRight, xLine, coord_x_list[-1],
                                                                 coord_y_list[-1])
        print(f"the r_rpm,theta_rpm: {r_rpm},{theta_rpm}")

        object_dict['r'] = r_rpm
        object_dict['theta'] = theta_rpm
        data = order_master.order_generate(object_dict['action'], object_dict['r'], object_dict['theta'],
                                           object_dict['object'])

        serial_communication.send_data(data)
        print("========================================")

    cvui.update()

    cv.namedWindow(win_name_cvui, cv.WINDOW_NORMAL)
    cv.imshow(win_name_cvui, cvui_img)
    cv.namedWindow(main_ui, cv.WINDOW_AUTOSIZE)
    cv.setMouseCallback(main_ui, on_EVENT_LBUTTONDOWN)
    cv.imshow(main_ui, frame_cat)
    cv.moveWindow(main_ui, start_X, start_Y)
    cv.moveWindow(win_name_cvui, start_X + frame_width, start_Y)

    if cv.waitKey(30) & 0xff == 27:
        serial_communication.close_engine()
        cv.destroyAllWindows()
        capL.release()
        capR.release()
        break
