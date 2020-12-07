"""
 @Author       :linyu
 @File         :color_detect.py
 @Description  :
 @Software     :PyCharm
"""

from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2 as cv

colors = OrderedDict({
    "black": (0, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "pink": (255, 192, 203),
    "brown": (210, 180, 140),
    "yellow": (255, 255, 0)})

class ColorLabeler:
    def __init__(self):
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []
        for (i, (name, rgb)) in enumerate(colors.items()):
            self.lab[i] = rgb
            self.colorNames.append(name)
        self.lab = cv.cvtColor(self.lab, cv.COLOR_RGB2LAB)

    def label(self, image, color):
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv.drawContours(mask, [color], -1, 255, -1)
        mask = cv.erode(mask, None, iterations=2)
        mean = cv.mean(image, mask=mask)[:3]
        minDist = (np.inf, None)
        for (i, row) in enumerate(self.lab):
            d = dist.euclidean(row[0], mean)
            if d < minDist[0]:
                minDist = (d, i)
        return self.colorNames[minDist[1]]
