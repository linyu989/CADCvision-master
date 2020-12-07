"""
 @Author       :linyu
 @File         :order_master.py
 @Description  :
 @Software     :PyCharm
"""

import cv2 as cv
import numpy as np
from order import coord_calibrate
import cvui


def order_generate(action, r=0.0, theta=0.0, object=None):
    data = "undefined"
    data = '*' + action + object + str(r) + 'p' + str(theta) + 's' + 'E'

    return data


def coord_get(img):
    a = []
    b = []

    def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            a.append(x)
            b.append(y)
            cv.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
            cv.putText(img, xy, (x, y), cv.FONT_HERSHEY_PLAIN,
                       1.0, (0, 0, 0), thickness=1)
            cv.imshow("image", img)
            print(a[-1], b[-1])
        return a, b

    cv.namedWindow("image")
    cv.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    cv.imshow("image", img)

    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()
    print(a, b, "ssss")


def button_click(frame, win_name_cvui):
    cvui.init(win_name_cvui)
    h, w = frame.shape[:2]
    start_col = w - 100
    start_row = 50
    button_width = 50
    button_height = 30
    setting_col = start_col - 20
    setting_row = start_row - 30
    setting_width = button_width + 40
    setting_height = button_height * 12

    frame[int(h / 2 - 1):int(h / 2 + 1)][:] = [0, 255, 0]
    for i in range(0, h):
        frame[i][int(w / 2 - 1):int(w / 2 + 1)] = [0, 255, 0]

    object = "undefined"

    while True:

        cvui.window(frame, setting_col, setting_row, setting_width, setting_height, "Setting")

        if (cvui.button(frame, start_col, start_row, button_width, button_height, "Ball")):
            object = "B"
            print("ball clicked")
        if (cvui.button(frame, start_col, start_row + 50, button_width, button_height, "Rubick")):
            object = "R"
            print("rubick clicked")
        if (cvui.button(frame, start_col, start_row + 100, button_width, button_height, "Up")):
            object = "U"
            print("Up clicked")
        if (cvui.button(frame, start_col, start_row + 150, button_width, button_height, "Down")):
            object = "D"
            print("Down clicked")

        if (cvui.button(frame, start_col, start_row + 250, button_width, button_height, "Send")):
            object = "S"
            print("Send clicked")

        cvui.update()

        cv.namedWindow(win_name_cvui, cv.WINDOW_NORMAL)
        cv.imshow(win_name_cvui, frame)
        cv.waitKey(0)


def coord_get_video(path):
    a, b = [0], [0]
    main_ui = "mainui"
    win_name_cvui = "cvui"
    frame = None

    def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            a.append(x)
            b.append(y)
            cv.circle(frame, (x, y), 1, (0, 0, 255), thickness=-1)
            cv.putText(frame, xy, (x, y), cv.FONT_HERSHEY_PLAIN,
                       1.0, (0, 0, 0), thickness=1)
            cv.imshow("image", frame)
            print(a[-1], b[-1])
        return a, b

    cap = cv.VideoCapture(path)

    cvui.init(win_name_cvui)

    while True:

        ret, frame = cap.read()

        h, w = frame.shape[:2]
        start_col = w - 100
        start_row = 50
        button_width = 50
        button_height = 30
        setting_col = start_col - 20
        setting_row = start_row - 30
        setting_width = button_width + 40
        setting_height = button_height * 12
        object = "undefined"

        frame[int(h / 2 - 1):int(h / 2 + 1)][:] = [0, 255, 0]
        for i in range(0, h):
            frame[i][int(w / 2 - 1):int(w / 2 + 1)] = [0, 255, 0]

        cvui.window(frame, setting_col, setting_row, setting_width, setting_height, "Setting")

        if (cvui.button(frame, start_col, start_row, button_width, button_height, "Ball")):
            object = "B"
            print("ball clicked")
        if (cvui.button(frame, start_col, start_row + 50, button_width, button_height, "Rubick")):
            object = "R"
            print("rubick clicked")
        if (cvui.button(frame, start_col, start_row + 100, button_width, button_height, "Up")):
            object = "U"
            print("Up clicked")
        if (cvui.button(frame, start_col, start_row + 150, button_width, button_height, "Down")):
            object = "D"
            print("Down clicked")

        if (cvui.button(frame, start_col, start_row + 250, button_width, button_height, "Send")):
            object = "S"
            print("Send clicked")

        cvui.update()

        cv.namedWindow(win_name_cvui, cv.WINDOW_NORMAL)
        cv.imshow(win_name_cvui, frame)

        cv.namedWindow("image", cv.WINDOW_NORMAL)
        cv.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
        cv.imshow("image", frame)
        print(a[-1], b[-1], "ss")

        if cv.waitKey(300) & 0xff == 27:
            cv.destroyAllWindows()
            break


if __name__ == '__main__':
    data = order_generate('z', 2000, 300, 'q')
    print(data)
