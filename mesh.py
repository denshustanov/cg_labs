import numpy as np
from tqdm import tqdm

from util import normal


# mesh class
# contains objet vertices, polygons and normals
# implements .obj file reading and preparation
class Mesh:
    def __init__(self):
        self.vertices = []
        self.polygons = []
        self.polygon_normals = []
        self.vertex_normals = []
        self.vertex_textures = []
        self.polygons_vertex_textures = []

    def read(self, path: str):
        with open(path) as obj_file:
            for line in tqdm(obj_file.readlines()):
                t = line.split()
                if len(t) > 1:
                    if t[0] == 'v':
                        self.vertices.append(np.array(list(map(float, t[1:4]))))
                    if t[0] == 'f':
                        polygon = [int(s.split('/')[0]) for s in t[1:4]]
                        self.polygons.append(polygon)

                        polygon_vt = [int(s.split('/')[1]) for s in t[1:4]]
                        # print(polygon_vt)
                        self.polygons_vertex_textures.append(polygon_vt)

                    if t[0] == 'vt':
                        self.vertex_textures.append((float(t[1]), float(t[2])))
            for i in tqdm(range(len(self.polygons))):
                self.polygon_normals.append(self.calc_polygon_normal(i))
            if len(self.vertices) != len(self.vertex_normals):
                self.vertex_normals = []
                for i in tqdm(range(len(self.vertices))):
                    self.vertex_normals.append(self.calc_vertex_normal(i+1))
        print(len(self.vertices), len(self.vertex_normals), len(self.vertex_textures))

    def get_polygon_points(self):
        return [
            np.array(list(map(lambda index: self.vertices[index-1], polygon))) for polygon in self.polygons
        ]

    def calc_polygon_normal(self, index: int):
        polygon = self.polygons[index]
        points_data = list(map(lambda i: self.vertices[i - 1], polygon))
        return normal(points_data)

    def calc_vertex_normal(self, index: int):
        v_normal = np.array([0, 0, 0], dtype=np.float64)
        c = 0
        for i in range(len(self.polygons)):
            if index in self.polygons[i]:
                v_normal += self.polygon_normals[i]
                c += 1
        return v_normal/c





