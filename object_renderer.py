import numpy as np
from tqdm import tqdm

from canvas import Canvas
from object import Object
from polygon_renderer import PolygonRenderer
from projection import Projection
from util import baricentric, normal_scalar_mul


# object renderer class
# implements z-buffer, Pong diffuse shading, diffuse texturing (uv-mapping)
class ObjectRenderer:
    def __init__(self, canvas: Canvas, projection: Projection):
        self.canvas = canvas
        self.projection = projection
        h, w, _ = canvas.shape()
        self.z_buffer = np.ones((h, w)) * 1000

    # render object on viewport
    def render(self, obj: Object, light_vector, color):
        self.canvas.clear()
        h, w, _ = self.canvas.shape()
        self.z_buffer = np.ones((h, w)) * 1000
        mesh = obj.mesh
        h, w, _ = self.canvas.shape()
        has_texture = obj.texture is not None and len(mesh.vertex_textures) >= len(mesh.vertices)

        # render mesh polygons
        for p_index, polygon in enumerate(tqdm(mesh.polygons)):

            # get polygon vertices
            points_data = list(map(lambda index: mesh.vertices[index - 1], polygon))

            # project polygon on viewport
            projected = [self.projection.project(vertex, w, h) for vertex in points_data]

            # calculate bbox
            x_min = int(np.clip(min(projected, key=lambda vertex: vertex[0])[0], 0, w))
            y_min = int(np.clip(min(projected, key=lambda vertex: vertex[1])[1], 0, h))
            x_max = int(np.clip(max(projected, key=lambda vertex: vertex[0])[0], 0, w))
            y_max = int(np.clip(max(projected, key=lambda vertex: vertex[1])[1], 0, h))

            if x_max < w:
                x_max += 1
            if y_max < h:
                y_max += 1

            # polygon rastering
            for x in range(x_min, x_max):
                for y in range(y_min, y_max):

                    # baricentric coordinates of pixel in polygon
                    lambda0, lambda1, lambda2 = baricentric((x, y), projected)

                    if lambda0 > 0 and lambda1 > 0 and lambda2 > 0:
                        # calculating z-value
                        z = lambda0 * points_data[0][2] + lambda1 * points_data[1][2] + lambda2 * points_data[2][2]
                        # print(z)
                        # comparing with z-buffer value
                        if z < self.z_buffer[y, x]:
                            self.z_buffer[y, x] = z

                            # shading calculation
                            if light_vector is not None:
                                l0 = normal_scalar_mul(mesh.vertex_normals[polygon[0] - 1], light_vector)
                                l1 = normal_scalar_mul(mesh.vertex_normals[polygon[1] - 1], light_vector)
                                l2 = normal_scalar_mul(mesh.vertex_normals[polygon[2] - 1], light_vector)

                                # pixel illumination interpolation (Phong shader)
                                diffuse = lambda0 * l0 + lambda1 * l1 + lambda2 * l2

                                light_coeff = (diffuse + 0.5)/2

                                # UV-mapping of diffuse texture
                                if has_texture:
                                    th, tw, tc = obj.texture.shape

                                    # get vertex texture coordinates from object
                                    vertex_textures = mesh.polygons_vertex_textures[p_index]
                                    vt_data = list(map(lambda index: mesh.vertex_textures[index - 1], vertex_textures))

                                    # calculate uv-coordinates
                                    u = (lambda0 * vt_data[0][0]
                                         + lambda1 * vt_data[1][0]
                                         + lambda2 * vt_data[2][0])*tw
                                    v = (lambda0 * vt_data[0][1]
                                         + lambda1 * vt_data[1][1]
                                         + lambda2 * vt_data[2][1])*th

                                    # pixel value from diffuse texture and illumination
                                    color = obj.texture[th-int(v), int(u)]*light_coeff
                                else:
                                    # plain white if no diffuse texture
                                    cc = light_coeff * 255
                                    color = (cc, cc, cc)

                            # draw pixel
                            self.canvas.fill_pixel(x, y, color)
