import cv2
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
    CANVAS_X = 1000
    CANVAS_Y = 1000

    canvas = Canvas(CANVAS_X, CANVAS_Y, 3)
    projector = PerspectiveProjection(FOV_X, FOV_Y, 10, 1000)
    renderer = ObjectRenderer(canvas, projector)

    mesh = Mesh()
    mesh.read('objs/cat/cat_low.obj')

    img = cv2.imread('objs/cat/Cat_diffuse.jpg')

    obj = Object(mesh, texture=img)
    obj.transform.shift_z = 10
    obj.transform.shift_y = -2

    obj.transform.rot_y = 150 / 360 * 2 * np.pi
    # obj.transform.rot_x = 90 / 360 * 2 * np.pi

    obj.transform.scale_x = 0.1
    obj.transform.scale_y = 0.1
    obj.transform.scale_z = 0.1

    l2 = np.array([-1, -1, 1])
    renderer.render(obj, l2, None)
    # for i in range(360//5):
    #     obj.transform.rot_y = i*5 / 360 * 2 * np.pi
    #     obj.transform.rot_x = i * 5 / 360 * 2 * np.pi
    #     renderer.render(obj, l2, None)
    canvas.save('imgs/cat.png')


if __name__ == '__main__':
    perspective_test()
