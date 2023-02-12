from abc import ABC, abstractmethod

import numpy as np


class Projection(ABC):
    @abstractmethod
    def project(self, point, w, h):
        pass


class StupidProjection(Projection):
    def __init__(self, x_shift, y_shift, x_scale, y_scale):
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.x_scale = x_scale
        self.y_scale = y_scale

    def project(self, point, w, h):
        x, y = self.x_scale * point[0] + self.x_shift, -self.y_scale * point[1] + self.y_shift
        return x, y


class PerspectiveProjection(Projection):
    def __init__(self, fov_x, fov_y, near, far):
        self.fov_x = fov_x
        self.fov_y = fov_y
        self.near = near
        self.far = far

        self.ex = 1 / np.tan(fov_x / 2)
        self.ey = 1 / np.tan(fov_y / 2)

    def project(self, point, w, h):
        u = w // 2 + self.ex * point[0] / point[2] * w
        v = h // 2 - self.ey * point[1] / point[2] * h
        return u, v
