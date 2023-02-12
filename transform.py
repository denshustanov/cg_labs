import numpy as np


class Transform:
    def __init__(self, shift_x, shift_y, shift_z, rx, ry, rz, scale_x, scale_y, scale_z):
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.shift_z = shift_z
        self.__rot_x = rx
        self.__rot_y = ry
        self.__rot_z = rz
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scale_z = scale_z

        self.__rot_matrix = Transform.__rot_matrix(self.rot_x, self.rot_y, self.rot_z)

    def transform(self, vertex):
        scale_vec = np.array([self.scale_x, self.scale_y, self.scale_z])
        return np.multiply(np.dot(vertex, self.__rot_matrix), scale_vec) + \
            np.array([self.shift_x, self.shift_y, self.shift_z])

    def rotate(self, vector):
        return np.dot(vector, self.__rot_matrix)

    @property
    def rot_x(self):
        return self.__rot_x

    @rot_x.setter
    def rot_x(self, angle: float):
        self.__rot_x = angle
        self.__rot_matrix = Transform.__rot_matrix(self.rot_x, self.__rot_y, self.__rot_z)

    @property
    def rot_y(self):
        return self.__rot_y

    @rot_y.setter
    def rot_y(self, angle: float):
        self.__rot_y = angle
        self.__rot_matrix = Transform.__rot_matrix(self.rot_x, self.__rot_y, self.__rot_z)

    @property
    def rot_z(self):
        return self.__rot_x

    @rot_z.setter
    def rot_z(self, angle: float):
        self.__rot_z = angle
        self.__rot_matrix = Transform.__rot_matrix(self.rot_x, self.__rot_y, self.__rot_z)

    @staticmethod
    def __rot_matrix(x, y, z):
        a = np.array([
            [1, 0, 0],
            [0, np.cos(x), -np.sin(x)],
            [0, np.sin(x), np.cos(x)]
        ])

        b = np.array([
            [np.cos(y), 0, np.sin(y)],
            [0, 1, 0],
            [-np.sin(y), 0, np.cos(y)]
        ])

        c = np.array([
            [np.cos(z), -np.sin(z), 0],
            [np.sin(z), np.cos(z), 0],
            [0, 0, 1]
        ])

        return np.dot(np.dot(a, b), c)

    @staticmethod
    def uniform():
        return Transform(0, 0, 0, 0, 0, 0, 1, 1, 1)
