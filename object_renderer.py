import numpy as np
from tqdm import tqdm

from canvas import Canvas
from object import Object
from polygon_renderer import PolygonRenderer
from projection import Projection
from util import baricentric, normal_scalar_mul


class ObjectRenderer:
    def __init__(self, canvas: Canvas, projection: Projection):
        self.canvas = canvas
        self.projection = projection
        h, w, _ = canvas.shape()
        self.z_buffer = np.ones((h, w))*1000

    def render(self, obj: Object, light_vector, color):
        mesh = obj.mesh
        h, w, _ = self.canvas.shape()
        for polygon in tqdm(mesh.polygons):
            points_data = list(map(lambda index: mesh.vertices[index-1], polygon))
            projected = [self.projection.project(vertex, w, h) for vertex in points_data]

            x_min = int(np.clip(min(projected, key=lambda vertex: vertex[0])[0], 0, w))
            y_min = int(np.clip(min(projected, key=lambda vertex: vertex[1])[1], 0, h))
            x_max = int(np.clip(max(projected, key=lambda vertex: vertex[0])[0], 0, w))
            y_max = int(np.clip(max(projected, key=lambda vertex: vertex[1])[1], 0, h))

            if x_max < w:
                x_max += 1
            if y_max < h:
                y_max += 1

            cc = normal_scalar_mul(mesh.polygon_normals[mesh.polygons.index(polygon)], light_vector)*255
            color = (cc, cc, cc)
            # print(color)

            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    # try:
                    lambda0, lambda1, lambda2 = baricentric((x, y), projected)
                    if lambda0 > 0 and lambda1 > 0 and lambda2 > 0:
                        z = lambda0 * points_data[0][2] + lambda1 * points_data[1][2] + lambda2 * points_data[2][2]
                        # print(z)
                        if z < self.z_buffer[y, x]:
                            self.z_buffer[y, x] = z
                            # if light_vector is not None:
                            #     # l0 = normal_scalar_mul(mesh.vertex_normals[polygon[0] - 1], light_vector)
                            #     # l1 = normal_scalar_mul(mesh.vertex_normals[polygon[1] - 1], light_vector)
                            #     # l2 = normal_scalar_mul(mesh.vertex_normals[polygon[2] - 1], light_vector)
                            #     # cc = (lambda0*l0 + lambda1*l1 + lambda2*l2)*255
                            #     cc = normal_scalar_mul(mesh.polygons[mesh.polygons.index(polygon)], light_vector)
                            #     color = (cc, cc, cc)
                            self.canvas.fill_pixel(x, y, color)





