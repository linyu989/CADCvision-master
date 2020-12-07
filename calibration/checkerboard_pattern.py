"""
 @Author       :linyu
 @File         :checkerboard_pattern.py
 @Description  :
 @Software     :PyCharm
"""

import cv2 as  cv
import numpy as np


def checkerboard(width, height, cell):
    width_pix = (width + 1) * cell + cell
    height_pix = (height + 1) * cell + cell
    image = np.zeros((height_pix, width_pix, 3), dtype=np.uint8)
    image.fill(255)
    win_name = "chessboard"
    cv.namedWindow("chessboard", cv.WINDOW_AUTOSIZE)
    cv.imshow(win_name, image)
    color = (255, 255, 255)
    fill_color = 0
    for j in range(1, height + 1):
        y = j * cell
        for i in range(1, width + 3):
            x0 = i * cell
            y0 = y
            rect_start = (x0, y0)
            x1 = x0 + cell
            y1 = y0 + cell
            rect_end = (x1, y1)
            cv.rectangle(image, rect_start, rect_end, color, 1, 0)
            image[y0:y1, x0:x1] = fill_color
            if (width % 2) and (i != width):
                fill_color = (0 if (fill_color == 255) else 255)
            elif i != width + 1:
                fill_color = (0 if (fill_color == 255) else 255)

    cv.imwrite(f"./calibration/chessboard_(w,h)_({width}x{height}).jpg", image)
    cv.imshow(win_name, image)
    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()


if __name__ == '__main__':
    checkerboard(8, 7, 100)
