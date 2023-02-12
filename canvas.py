import numpy as np
import cv2
from typing import Iterable

from util import baricentric


class Canvas:
    def __init__(self, w: int, h: int, c: int):
        self.__canvas = np.zeros((h, w, c))
        self.__z_buffer = np.ones((h, w))*255

    def shape(self):
        return self.__canvas.shape

    def fill_pixel(self, x: int, y: int, v):
        c = self.__canvas.shape[2]
        for i in range(c):
            self.__canvas[y, x, i] = v[i]

    def draw_line(self, start, end, color):
        x0, y0 = start
        x1, y1 = end

        if x0 == x1 and y0 == y1:
            self.fill_pixel(x0, y0, color)
            return

        steep = False

        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1, = y1, x1
            steep = True

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = y1 - y0
        derror = abs(dy / dx)
        error = 0
        y = y0

        for x in range(x0, x1):
            if (steep):
                self.fill_pixel(y, x, color)
            else:
                self.fill_pixel(x, y, color)
            error += derror

            if error > 0.5:
                y += 1 if y1 > y0 else -1
                error -= 1

    def draw_triangle(self, v1, v2, v3, color):
        x1, y1 = v1
        x2, y2 = v2
        x3, y3 = v3

        h, w, _ = self.__canvas.shape

        x_min = int(max(0, min(x1, x2, x3)))
        y_min = int(max(0, min(y1, y2, y3)))
        x_max = int(min(w, max(x1, x2, x3)))
        y_max = int(min(h, max(y1, y2, y3)))

        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                # try:
                    l0, l1, l2 = baricentric((x, y), (v1, v2, v3))
                    if l0 > 0 and l1 > 0 and l2 > 0:
                        self.fill_pixel(x, y, color)
                # except Exception:
                    # print(x, y, v1, v2, v3)

    def save(self, path: str):
        cv2.imwrite(path, self.__canvas)

    def get(self):
        return self.__canvas
