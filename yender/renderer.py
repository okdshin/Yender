import yender.renderer_impl as impl
import numpy as np

def raytrace(image_size, origin, f, yaw, pitch, triangles, colors):
    '''Render image with raytracing

    Args:
        image_size (Tuple of two ints): (width, height)
        origin (Tuple of three ints): the start point (x, y, z) of rays
        f (float): focal length
        yaw (float): camera yaw (angle)
        pitch (float): camera pitch (angle)
        triangles: triangles[i] corresponding to colors[i]
        colors: colors[i] corresponding to triangles[i]

    Returns:
        list of list of list of int: rendered image (channel, x, y)
    '''
    return impl.raytrace2(image_size[0], image_size[1], origin, f, yaw, pitch, triangles, colors)

def box_triangles(color):
    '''Make triangles of a box

    Args:
        color (tuple of three ints): triangle color

    Returns:
        tuple of triangles and colors
    '''
    triangles = np.asarray([
        [(0,0,0), (1,0,0), (0,0,1)],
        [(1,0,1), (0,0,1), (1,0,0)],
        [(0,1,0), (0,1,1), (1,1,0)],
        [(1,1,1), (1,1,0), (0,1,1)],

        [(0,0,0), (0,1,0), (1,0,0)],
        [(1,1,0), (1,0,0), (0,1,0)],
        [(0,0,1), (1,0,1), (0,1,1)],
        [(1,1,1), (0,1,1), (1,0,1)],

        [(0,0,0), (0,0,1), (0,1,0)],
        [(0,1,1), (0,1,0), (0,0,1)],
        [(1,0,0), (1,1,0), (1,0,1)],
        [(1,1,1), (1,0,1), (1,1,0)],
    ])
    colors = [color for _ in range(len(triangles))]
    return triangles, colors

def tile_triangles(color):
    '''Make triangles of a tile

    Args:
        color (tuple of three ints): triangle color

    Returns:
        tuple of triangles and colors
    '''
    triangles = np.array([
        [(0,0,0), (1,0,0), (0,1,0)],
        [(1,1,0), (0,1,0), (1,0,0)],
    ])+np.asarray([0,0,0.01])
    colors = [color for _ in range(len(triangles))]
    return triangles, colors

