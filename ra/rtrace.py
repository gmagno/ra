
import numpy as np


def ray_x_plane(r0, rd, pp, pn, tol=1e-6):
    '''Determines the intersection between a ray, defined by its origin
        position `r0` and direction vector `rd`, and a plane defined by its
        normal vector `pn` and a point `pp`. The distance from the ray's origin
        to the intersection point is computed and returned.

    Parameters
    ----------
    r0: a numpy.ndarray with shape (3,) representing the ray origin position
    rd: a numpy.ndarray with shape (3,) representing the ray direction vector
    pp: a numpy.ndarray with shape (3,) representing a point belonging to the
        plane
    pn: a numpy.ndarray with shape (3,) representing the plane normal vector
    tol: a float representing the tolerance when computing the dot product
        `vd`.

    Returns
    -------
    A float representing distance from the ray's origin to the intersection
    point between the ray and the plane. If the ray and plane do not intersect
    `inf` is returned. If the ray hits the plane's back `inf` is also returned.
    '''
    vd = np.dot(pn, rd)

    if np.abs(vd) < tol:
        return np.inf
    v0 = np.dot(pn, pp - r0)
    t = v0 / vd

    # ensure `tol` is not too small otherwise there will be unwanted
    # reflections due to rays starting behind walls
    if t < 1e-3:
        return np.inf
    return t


def point_in_polygon(ri, poly_verts, pn):
    '''Checks if a point `ri` is inside a polygon defined by its vertices
    `poly_verts` and normal vector `pn`.

    Parameters
    ----------
    ri: a numpy.ndarray with shape (3,) representing the point coordinates to
        check if belongs to the polygon defined by `poly_verts`.
    poly_verts: a numpy.ndarray with shape (N, 3) representing the polygon's
    vertices.
    pn: a numpy.ndarray with shape (3,) representing the polygon normal vector.

    Returns
    -------
    True if `ri` is inside the polygon.
    '''
    throw_away = np.argmax(np.abs(pn))
    poly_verts_uv = poly_verts - ri
    # TODO: avoid the delete to speed up a bit
    poly_verts_uv = np.delete(poly_verts_uv, throw_away, 1)
    # ri_uv = np.delete(ri, throw_away, 0)
    nverts = poly_verts_uv.shape[0]  # number of vertices
    nc = 0  # number of crossings
    for a, v in enumerate(poly_verts_uv):
        nv = poly_verts_uv[(a+1) % nverts]  # nv: next vert, v: current vert)
        sh = -1 if v[1] < 0 else 1
        nsh = -1 if nv[1] < 0 else 1
        if sh != nsh:
            if v[0] > 0 and nv[0] > 0:
                nc += 1
            elif v[0] > 0 or nv[0] > 0:
                if v[0] - v[1] * (nv[0] - v[0]) / (nv[1] - v[1]) > 0:
                    nc += 1
    return nc % 2  # no need to cast, in python3 True is 1, False is 0


def ray_x_polygon(r0, rd, poly_verts, pn, tol=1e-6):
    '''

    Parameters
    ----------
    r0, rd, pn, tol: check function `ray_x_plane()` parameters.
    poly_verts: check function `point_in_polygon()` parameters.

    Returns
    -------
    A 3-tuple where the first element represents the distance from the ray's
        origin to the intersection point, the second one the coordinates of the
        intersection point, and the third one a boolean set to True if the ray
        intersects the polygon
    '''
    t = ray_x_plane(r0, rd, poly_verts[0], pn, tol)
    # the following instruction will trigger a "RuntimeWarning: invalid value
    # encountered in multiply" message if t == inf
    ri = r0 + rd*t
    if t == np.inf:
        return t, ri, False
    is_inside = point_in_polygon(ri, poly_verts, pn)
    return t, ri, is_inside


def ray_x_sphere(r0, rd, sc, sr):
    '''
    Parameters
    ----------
    r0: a numpy.ndarray with shape (3,) representing the ray origin position
    rd: a numpy.ndarray with shape (3,) representing the ray direction vector
    sc: a numpy.ndarray with shape (3,) representing the sphere center
        coordinates
    sr: a scalar representing the sphere radius
    '''
    oc = sc - r0
    l2oc = np.dot(oc, oc)  # ray to the sphere center squared distance
    if l2oc >= sr * sr:  # check if ray originates outside the sphere
        # determine the closest approach along the ray to the sphere's center
        tca = np.dot(oc, rd)
        if tca >= 0:
            t2hc = sr*sr - l2oc + tca*tca
            if t2hc > 0:
                t = tca - np.sqrt(t2hc)
                ri = r0 + rd*t  # the intersection point
                return ri, True
    return np.inf, False
