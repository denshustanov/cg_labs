import numpy as np

from mesh import Mesh
from transform import Transform
from copy import deepcopy


class Object:
    def __init__(self, mesh: Mesh, texture: np.ndarray = None):
        self.transform = Transform.uniform()
        self.__mesh = mesh
        self.__texture = texture

    @property
    def mesh(self) -> Mesh:
        new_mesh = deepcopy(self.__mesh)

        for i in range(len(new_mesh.vertices)):
            new_mesh.vertices[i] = self.transform.transform(new_mesh.vertices[i])
            n = new_mesh.vertex_normals[i]
            new_mesh.vertex_normals[i] = self.transform.rotate(new_mesh.vertex_normals[i])
            # new_mesh.polygon_normals

        for i in range(len(new_mesh.polygon_normals)):
            new_mesh.polygon_normals[i] = self.transform.rotate(new_mesh.polygon_normals[i])
        return new_mesh

    @property
    def texture(self) -> np.ndarray:
        return self.__texture

