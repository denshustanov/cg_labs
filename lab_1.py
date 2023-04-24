import numpy as np
from canvas import  Canvas
from mesh import Mesh
from util import stupid_project_vertex


# draw lines with bresenham algorithm
def test_bresenham_satanic():
    c = Canvas(100, 100, 3)
    r = 30
    angles = [(90 + 72 * i) * (2 * np.pi) / 360 for i in range(5)]
    points = [(int(30 * np.cos(a)) + 50, -int(30 * np.sin(a)) + 50) for a in angles]

    for i in range(5):
        c.draw_line(points[i], points[(i + 2) % 5], (0, 0, 255))
        c.draw_line(points[i], points[(i + 1) % 5], (0, 0, 255))

    path = 'imgs/pentagram.png'
    c.save(path)

# read obj file and render mesh vertices
def test_obj_read_vertices():
    o = Mesh()
    o.read('test.obj')

    print(len(o.vertices))

    c = Canvas(2000, 2000, 3)

    for v in o.vertices:
        x, y, = stupid_project_vertex(v)
        c.fill_pixel(x, y, (255, 255, 255))

    c.save('test_vertices.png')

# read obj file and render mesh edges
def test_obj_read_edges():
    o = Mesh()
    o.read('test.obj')

    print(len(o.vertices))

    c = Canvas(2000, 2000, 3)

    for polygon in o.polygons:
        for i in range(3):
            try:
                p1 = polygon[i]
                p2 = polygon[(i+1) % 3]
                v1 = o.vertices[p1-1]
                v2 = o.vertices[p2-1]
                c.draw_line(stupid_project_vertex(v1), stupid_project_vertex(v2), (255, 255, 255))
            except Exception:
                pass


    c.save('test_edges.png')
