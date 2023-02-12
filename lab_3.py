import numpy as np
from tqdm import tqdm

from canvas import Canvas
from mesh import Mesh
from object import Object
from projection import PerspectiveProjection
from object_renderer import ObjectRenderer


def perspective_test():
    FOV_X = 90 / 360 * (2 * np.pi)
    FOV_Y = 90 / 360 * (2 * np.pi)
    CANVAS_X = 500
    CANVAS_Y = 500

    canvas = Canvas(CANVAS_X, CANVAS_Y, 3)
    projector = PerspectiveProjection(FOV_X, FOV_Y, 10, 1000)
    renderer = ObjectRenderer(canvas, projector)

    mesh = Mesh()
    mesh.read('objs/test.obj')

    obj = Object(mesh)
    obj.transform.shift_z = 4
    obj.transform.shift_y = -1

    obj.transform.rot_y = 90 / 360 * 2 * np.pi

    obj.transform.scale_x = 20
    obj.transform.scale_y = 20
    obj.transform.scale_z = 20

    l2 = np.array([-1, -1, 1])
    renderer.render(obj, l2, None)

    canvas.save('imgs/perspective_with_gouraud.png')


if __name__ == '__main__':
    perspective_test()
