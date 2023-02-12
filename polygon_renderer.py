import numpy as np

from canvas import Canvas
from projection import Projection
from util import baricentric, normal_scalar_mul


class PolygonRenderer:
    def __init__(self, canvas: Canvas, projector: Projection):
        h, w, _ = canvas.shape()
        self.__canvas = canvas
        self.__z_buffer = np.ones((h, w)) * 100000
        self.projector = projector

    def draw_polygon(self, polygon, color, light_vec=None):
        # v1, v2, v3 = polygon
        h, w, _ = self.__canvas.shape()
        projected = [self.projector.project(vertex, w, h) for vertex in polygon]

        x_min = int(np.clip(min(projected, key=lambda vertex: vertex[0])[0], 0, w))
        y_min = int(np.clip(min(projected, key=lambda vertex: vertex[1])[1], 0, h))
        x_max = int(np.clip(max(projected, key=lambda vertex: vertex[0])[0], 0, w))
        y_max = int(np.clip(max(projected, key=lambda vertex: vertex[1])[1], 0, h))

        if x_max < w:
            x_max += 1
        if y_max < h:
            y_max += 1

        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                # try:
                l0, l1, l2 = baricentric((x, y), projected)
                if l0 > 0 and l1 > 0 and l2 > 0:
                    z = l0 * polygon[0][2] + l1 * polygon[1][2] + l2 * polygon[2][2]
                    print(z)
                    if z < self.__z_buffer[y, x]:
                        self.__z_buffer[y, x] = z
                        if light_vec is not None:
                            l1 = normal_scalar_mul()
                        self.__canvas.fill_pixel(x, y, color)
                        # print(x, y, color)
