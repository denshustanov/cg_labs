from mesh import Mesh
from transform import Transform
from copy import deepcopy


class Object:
    def __init__(self, mesh: Mesh):
        self.transform = Transform.uniform()
        self.__mesh = mesh

    @property
    def mesh(self) -> Mesh:
        new_mesh = deepcopy(self.__mesh)

        for i in range(len(new_mesh.vertices)):
            new_mesh.vertices[i] = self.transform.transform(new_mesh.vertices[i])
            # new_mesh.vertex_normals[i] = self.transform.rotate(new_mesh.vertex_normals[i])
        return new_mesh

