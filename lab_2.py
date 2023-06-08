from mesh import Mesh
from canvas import Canvas
import numpy as np

from polygon_renderer import PolygonRenderer
from projection import StupidProjection
from util import stupid_project_vertex, normal
from tqdm import tqdm


#
def obj_polys_test():
    o = Mesh()
    o.read('objs/test.obj')

    c = Canvas(2000, 2000, 3)
    l = np.array([0, 0, 1])
    l2 = np.array([-1, -1, -1])
    l2_norm = np.linalg.norm(l2)
    for polygon in tqdm(o.polygons):

        polygon_points = list(map(lambda v: o.vertices[v-1], polygon))
        poly_norm = normal(polygon_points)
        a = np.dot(l, poly_norm)/np.linalg.norm(poly_norm)
        if a < 0:
            light_coeff = np.dot(l2, poly_norm)/(np.linalg.norm(poly_norm)*l2_norm)
            color = (255*light_coeff, 255*light_coeff, 255*light_coeff)
            vertices = list(map(lambda v: stupid_project_vertex(o.vertices[v-1], to_int=False), polygon))
            v1, v2, v3 = vertices
            c.draw_triangle(v1, v2, v3, color)

    c.save("imgs/test_polys.png")


def z_buffer_render_test():
    obj = Mesh()
    obj.read('objs/test.obj')

    c = Canvas(2000, 2000, 3)
    projector = StupidProjection(1000, 1500, 8000, 8000)
    renderer = PolygonRenderer(c, projector)
    l = np.array([0, 0, 1])
    l2 = np.array([-1, -1, -1])
    l2_norm = np.linalg.norm(l2)
    for p in tqdm(obj.polygons):
        polygon_points = list(map(lambda v: obj.vertices[v - 1], p))
        poly_norm = normal(polygon_points)
        a = np.dot(l, poly_norm) / np.linalg.norm(poly_norm)
        # if a < 0:
        light_coeff = np.dot(l, poly_norm) / (np.linalg.norm(poly_norm) * l2_norm)
        color = (255 * light_coeff, 255 * light_coeff, 255 * light_coeff)
        renderer.draw_polygon(polygon_points, color)
    c.save('imgs/z_buffer_test.png')


if __name__ == '__main__':
    obj_polys_test()
    # z_buffer_render_test()
