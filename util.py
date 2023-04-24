import numpy as np

# get baricentric coordinates of point in polygon
def baricentric(point, polygon):
    v0, v1, v2 = polygon
    x0, y0 = v0
    x1, y1, = v1
    x2, y2 = v2
    x, y = point

    l0 = ((x1 - x2) * (y - y2) - (y1 - y2) * (x - x2)) / ((x1 - x2) * (y0 - y2) - (y1 - y2) * (x0 - x2))
    l1 = ((x2 - x0) * (y - y0) - (y2 - y0) * (x - x0)) / ((x2 - x0) * (y1 - y0) - (y2 - y0) * (x1 - x0))
    l2 = ((x0 - x1) * (y - y1) - (y0 - y1) * (x - x1)) / ((x0 - x1) * (y2 - y1) - (y0 - y1) * (x2 - x1))

    return l0, l1, l2


# prject vertex on viewport
def stupid_project_vertex(v, to_int=True):
    x, y = 8000 * v[0] + 1000, -8000 * v[1] + 1500
    if to_int:
        x, y = int(x), int(y)
    return x, y


# get normal vector of polygon
def normal(polygon):
    v0, v1, v2 = polygon

    x0, y0, z0 = v0
    x1, y1, z1 = v1
    x2, y2, z2 = v2

    return np.cross((x1-x0, y1-y0, z1-z0), (x1-x2, y1-y2, z1-z2))

# normalized scalar multiplication of two vectors
def normal_scalar_mul(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1)* np.linalg.norm(v2))
