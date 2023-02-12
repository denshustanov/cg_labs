import numpy as np


class Object3D:
    def __init__(self):
        self.vertices = []
        self.polygons = []

    def read(self, path: str):
        with open(path) as obj_file:
            for line in obj_file.readlines():
                t = line.split()
                if t[0] == 'v':
                    self.vertices.append(np.array(list(map(float, t[1:4]))))
                if t[0] == 'f':
                    polygon = [int(s.split('/')[0]) for s in t[1:]]
                    self.polygons.append(polygon)
