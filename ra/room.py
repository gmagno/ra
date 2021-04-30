import numpy as np
from scipy.spatial import ConvexHull
import collada as co
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import scipy.io as spio

from log import log
import ra_cpp

class GeometryApi():
    def __init__(self, geom_dict):
        '''
        Set up the room geometry from the blender or 3D geometry modelling soft.
        The input is a geometry dictionary.
        Geometry consists of: Volume, Total ara and an
        array of plane objects. Each plane object will be
        processed in a c++ class and have the following att:
        - name (string)
        - bounding box (bool)
        - list of vertices (Eigen<double> - Nvert x 3)
        - normal (Eigen<double> - 1 x 3)
        - vert_x - 2D polygon x coord (Eigen<double> - 1 x Nvert)
        - vert_y - 2D polygon y coord (Eigen<double> - 1 x Nvert)
        - nig - 2D normal components index (Eigen<int> - 1 x 2)
        - area (double)
        - centroid (Eigen<double> - 1 x 3)
        - alpha - absorption coefficient (Eigen<double> - 1 x Nfreq)
        - s - scattering coefficient (double)
        '''
        self.planes = []    # A list of planes (object with attributes)
        for jp in np.arange(0, len(geom_dict)):
            vert_x, vert_y, normal_nig = vert_2d(
                geom_dict[jp]['normal'], geom_dict[jp]['vertices'])
            # FIXME swap the next two lines. From matlab area comes from mat file
            # FIXME From blender a triangle comes and we calculate the area. 
            area = np.float64(geom_dict[jp]['area']) ### Matlab
            # area = np.float64(triangle_area(geom_dict[jp]['vertices']))   # blender
            ##############################################################
            centroid = np.float32(triangle_centroid(geom_dict[jp]['vertices']))
            # plane object
            plane = ra_cpp.Planecpp(geom_dict[jp]['name'],
                geom_dict[jp]['bbox'],
                geom_dict[jp]['vertices'],
                geom_dict[jp]['normal'],
                vert_x, vert_y, normal_nig, area, centroid,
                geom_dict[jp]['alpha'], geom_dict[jp]['s'])
            self.planes.append(plane)
        # total area and volume
        self.total_area = total_area(self.planes)
        self.volume = volume(self.planes)

class GeometryMat():
    def __init__(self, geo_cfg, alpha, s):
        '''
        Set up the room geometry from the .mat file
        Geometry consists of: Volume, Total ara and an
        array of plane objects. Each plane object will be
        processed in a c++ class and have the following att:
        - name (string)
        - bounding box (bool)
        - list of vertices (Eigen<double> - Nvert x 3)
        - normal (Eigen<double> - 1 x 3)
        - vert_x - 2D polygon x coord (Eigen<double> - 1 x Nvert)
        - vert_y - 2D polygon y coord (Eigen<double> - 1 x Nvert)
        - nig - 2D normal components index (Eigen<int> - 1 x 2)
        - area (double)
        - centroid (Eigen<double> - 1 x 3)
        - alpha - absorption coefficient (Eigen<double> - 1 x Nfreq)
        - s - scattering coefficient (double)
        '''
        # toml file and matlab data
        mat = spio.loadmat(geo_cfg['room'],
            struct_as_record = True)
        # mat = spio.loadmat(config['geometry']['room'], struct_as_record = True)
        vertcoord = np.array(mat['geometry']['vertcoord'][0][0])
        # Load an array of plane objects
        self.planes = []
        planes = mat['geometry']['plane'][0][0][0]
        for jp, p in enumerate(planes):
            # Get things from matlab data
            name = 'nameless matlab plane'
            vertices = []
            for v in p[0][0]:
                vertices.append(vertcoord[v-1])
            vertices  = np.array(vertices)
            normal = np.float32(p[1][0])
            vert_x, vert_y, normal_nig = vert_2d(normal, vertices)
            area = np.float64(p[2][0])
            centroid = np.float32(p[3][0])
            # try:
            alpha_v = np.float32(alpha[jp])
            ################### cpp plane class #################
            # log.info(jp)
            # log.info(normal_nig)
            plane = ra_cpp.Planecpp(name, False, vertices, normal,
                vert_x, vert_y, normal_nig, area, centroid,
                alpha_v, s[jp])
            ################### py plane class ################
            # plane = PyPlane(name, False, vertices, normal,
            #     vert_x, vert_y, normal_nig, area, centroid,
            #     alpha[jp], s[jp])
            # Append plane object
            self.planes.append(plane)
        # total area and volume
        self.total_area = np.array(mat['geometry']['TotalArea'][0][0][0][0])
        self.volume = np.array(mat['geometry']['Volume'][0][0][0][0])
        # The pet class was used for self instruction
        # pet = ra_cpp.Pet('pluto', 5)
        # log.info(pet.get_name())

    def plot_mat_room(self, normals='off'):
        '''
        a simple plot of the room using matplotlib - not redered
        '''
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        # loop through plane objects
        for plane in self.planes:
            # vertexes plot
            ax.scatter(plane.vertices[:,0], plane.vertices[:,1],
                plane.vertices[:,2], color='blue')
            verts = [list(zip(plane.vertices[:,0],
                plane.vertices[:,1], plane.vertices[:,2]))]
            # patch plot
            collection = Poly3DCollection(verts,
                linewidths=1, alpha=0.5, edgecolor = 'gray')
            face_color = 'silver' # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
            collection.set_facecolor(face_color)
            ax.add_collection3d(collection)
            # plot the normals if the user wants to
            if normals == 'on':
                ax.quiver(plane.centroid[0], plane.centroid[1],
                plane.centroid[2], plane.normal[0],
                plane.normal[1], plane.normal[2],
                length=1, color = 'red', normalize=True)
        # set axis labels
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show() # show plot

    def plot_raypath(self, sourcecoord, raypath, receivers):
        '''
        a simple plot of the room - not redered
        '''
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        # First plot the room
        for plane in self.planes:
            # vertexes plot
            ax.scatter(plane.vertices[:,0], plane.vertices[:,1],
                plane.vertices[:,2], color='black', s=5)
            # patch plot
            verts = [list(zip(plane.vertices[:,0],
                plane.vertices[:,1], plane.vertices[:,2]))]
            collection = Poly3DCollection(verts,
                linewidths=1, alpha=0.5, edgecolor = 'gray')
            face_color = 'silver' # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
            collection.set_facecolor(face_color)
            ax.add_collection3d(collection)
        # plot the sound source
        ax.scatter(sourcecoord[0], sourcecoord[1], sourcecoord[2],
            color='black',  marker = "*", s=500)
        # plot receivers
        for rec in receivers:
            ax.scatter(rec.coord[0], rec.coord[1],
                rec.coord[2], color='blue', s=100)

        # plot the ray path
        ray_vec = raypath[0,:]-sourcecoord
        arrow_length = np.linalg.norm(ray_vec)
        ax.quiver(sourcecoord[0], sourcecoord[1], sourcecoord[2],
                ray_vec[0], ray_vec[1], ray_vec[2],
                arrow_length_ratio = 0.006 * arrow_length)
        N_max_ref = len(raypath)
        for jray in np.arange(N_max_ref-1):
            ray_origin = raypath[jray]
            ray_vec = raypath[jray+1]-raypath[jray]
            arrow_length = np.linalg.norm(ray_vec)
            ax.quiver(ray_origin[0], ray_origin[1], ray_origin[2],
                ray_vec[0], ray_vec[1], ray_vec[2],
                arrow_length_ratio = 0.006 * arrow_length)

            ax.scatter(raypath[jray,0], raypath[jray,1],
                raypath[jray,2], color='red', marker = "+")
        # set axis labels
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show() # show plot


class Geometry():
    def __init__(self, geo_cfg, alpha, s):
        '''
        Set up the room geometry from the .dae file
        Geometry consists of: Volume, Total ara and an
        array of plane objects. Each plane object will be
        processed in a c++ class and have the following att:
        - name (string)
        - bounding box (bool)
        - list of vertices (Eigen<double> - Nvert x 3)
        - normal (Eigen<double> - 1 x 3)
        - vert_x - 2D polygon x coord (Eigen<double> - 1 x Nvert)
        - vert_y - 2D polygon y coord (Eigen<double> - 1 x Nvert)
        - nig - 2D normal components index (Eigen<int> - 1 x 2)
        - area (double)
        - centroid (Eigen<double> - 1 x 3)
        - alpha - absorption coefficient (Eigen<double> - 1 x Nfreq)
        - s - scattering coefficient (double)
        '''
        # toml file
        daepath=geo_cfg['room']      # path to .dae
        # Load an array of plane objects
        self.planes = []    # A list of planes (object with attributes)
        mesh = co.Collada(daepath)
        for obj in mesh.scene.objects('geometry'): #loop every obj
            for triset in obj.primitives():        #loop every primitives
                # First if excludes the non-triangles objects
                if type(triset) != co.triangleset.BoundTriangleSet:
                    log.info('Warning: non-supported primitive ignored!')
                    continue
                # Loop trhough all triangles
                for jp, tri in enumerate(triset):
                    # Define a single plane object
                    name='{}-{}'.format(obj.original.name, jp)
                    vertices=np.array(tri.vertices)
                    normal=np.float32(tri.normals[0] /
                        np.linalg.norm(tri.normals[0]))
                    vert_x, vert_y, normal_nig = vert_2d(normal, vertices)
                    area = np.float64(triangle_area(vertices))
                    centroid = np.float32(triangle_centroid(vertices))
                    alpha_v = np.float32(alpha[jp])
                    ################### cpp plane class #################
                    plane = ra_cpp.Planecpp(name, False, vertices, normal,
                        vert_x, vert_y, normal_nig, area, centroid,
                        alpha_v, s[jp])
                    ################### py plane class ################
                    # plane = PyPlane(name, False, vertices, normal,
                    #     vert_x, vert_y, normal_nig, area, centroid,
                    #     alpha[jp], s[jp])
                    # Append plane object
                    self.planes.append(plane)
        # total area and volume
        self.total_area = total_area(self.planes)
        self.volume = volume(self.planes)

    def plot_dae_room(self, normals='off'):
        '''
        a simple plot of the room - not redered
        '''
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        for plane in self.planes:
            # vertexes plot
            ax.scatter(plane.vertices[:,0], plane.vertices[:,1],
                plane.vertices[:,2], color='blue')
            # patch plot
            verts = [list(zip(plane.vertices[:,0],
                plane.vertices[:,1], plane.vertices[:,2]))]
            collection = Poly3DCollection(verts,
                linewidths=1, alpha=0.5, edgecolor = 'gray')
            face_color = 'silver' # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
            collection.set_facecolor(face_color)
            ax.add_collection3d(collection)
            # plot the normals if the user wants to
            if normals == 'on':
                ax.quiver(plane.centroid[0], plane.centroid[1],
                plane.centroid[2], plane.normal[0],
                plane.normal[1], plane.normal[2],
                length=1, color = 'red', normalize=True)
        # set axis labels
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show() # show plot

    def plot_raypath(self, sourcecoord, raypath, receivers):
        '''
        a simple plot of the room - not redered
        '''
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        # First plot the room
        for plane in self.planes:
            # vertexes plot
            ax.scatter(plane.vertices[:,0], plane.vertices[:,1],
                plane.vertices[:,2], color='black', s=5)
            # patch plot
            verts = [list(zip(plane.vertices[:,0],
                plane.vertices[:,1], plane.vertices[:,2]))]
            collection = Poly3DCollection(verts,
                linewidths=1, alpha=0.5, edgecolor = 'gray')
            face_color = 'silver' # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
            collection.set_facecolor(face_color)
            ax.add_collection3d(collection)
        # plot the sound source
        ax.scatter(sourcecoord[0], sourcecoord[1], sourcecoord[2],
            color='black',  marker = "*", s=500)
        # plot receivers
        for rec in receivers:
            ax.scatter(rec.coord[0], rec.coord[1],
                rec.coord[2], color='blue', s=100)

        # plot the ray path
        ray_vec = raypath[0,:]-sourcecoord
        arrow_length = np.linalg.norm(ray_vec)
        ax.quiver(sourcecoord[0], sourcecoord[1], sourcecoord[2],
                ray_vec[0], ray_vec[1], ray_vec[2],
                arrow_length_ratio = 0.006 * arrow_length)
        N_max_ref = len(raypath)
        for jray in np.arange(N_max_ref-1):
            ray_origin = raypath[jray]
            ray_vec = raypath[jray+1]-raypath[jray]
            arrow_length = np.linalg.norm(ray_vec)
            ax.quiver(ray_origin[0], ray_origin[1], ray_origin[2],
                ray_vec[0], ray_vec[1], ray_vec[2],
                arrow_length_ratio = 0.006 * arrow_length)

            ax.scatter(raypath[jray,0], raypath[jray,1],
                raypath[jray,2], color='red', marker = "+")
        # set axis labels
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show() # show plot


class PyPlane():
    '''
    A class to define a single plane object with the following att:
    - name (string)
    - bounding box (bool)
    - list of vertices (Eigen<double> - Nvert x 3)
    - normal (Eigen<double> - 1 x 3)
    - vert_x - 2D polygon x coord (Eigen<double> - 1 x Nvert)
    - vert_y - 2D polygon y coord (Eigen<double> - 1 x Nvert)
    - nig - 2D normal components index (Eigen<int> - 1 x 2)
    - area (double)
    - centroid (Eigen<double> - 1 x 3)
    - alpha - absorption coefficient (Eigen<double> - 1 x Nfreq)
    - s - scattering coefficient (double)
    '''
    def __init__(self, name, bbox, vertices, normal,
        vert_x, vert_y, nig, area, centroid, alpha, s):
        self.name = name   # plane name 'default = matlab nameless plane
        self.bbox = bbox  # by default a plane is part of the room geometry
        self.vertices = vertices
        self.normal = normal
        # For point in polygon test we can do it in 2D
        # It is better to return a list of 2D vertexes once and for all
        self.vert_x = vert_x
        self.vert_y = vert_y
        self.nig = nig
        # area of each polygon
        self.area = area
        # centroid of a polygon
        self.centroid = centroid
        # The acoustical properties of the plane
        self.alpha = np.array(alpha, np.float32)
        self.s = s

def vert_2d(normal, vertcoord):
    '''
    Function to transform the 3D plane to 2D.
    Input: normal of the plane
    3D vertex coordinates of the plane (array of 1x3 arrays)
    Output: vert_x: a numpy array of x-coordinates of vertexes
            vert_y: a numpy array of y-coordinates of vertexes
            normal_nig: the index of the normal components used
            (this will be used when converting the reflection
            point from 3D to 2D)
    '''
    # Find biggest component of the normal - the component to ignore
    normal_abs = np.absolute(normal)
    normal_id_equal = np.where(normal_abs == normal_abs.max())
    normal_id_less = np.where(normal_abs < normal_abs.max())
    # log.info(normal_id_less)
    # log.info("components with max abs normal")
    # log.info(normal_id[0])
    # Find the index of the normal which are not ignored
    normal_nig = np.where(normal_abs != normal_abs.max())
    
    # normal_nig = np.intc(normal_nig[0]) # integers (index)
    if len(normal_id_equal[0]) == 1:
        normal_nig = np.intc(normal_nig[0]) # integers (index)
    else:
        vazio = []
        normal_id2 = np.delete(normal_id_equal, 0)
        vazio.append(normal_nig[0][0])
        vazio.append(normal_id2[0])
        normal_nig = np.intc(vazio)
    # Empty lists of x and y vertex coord
    vert_x = []
    vert_y = []
    for row in vertcoord:
        v = np.take(row, normal_nig)
        # if len(normal_id_equal[0]) == 1: # for 3 different normal components
        #     v = np.delete(row, normal_id_equal)
        #     # log.info(v)
        # else: # normal has equal components
        #     normal_id2 = np.delete(normal_id_equal, 0)
        #     # log.info("non deleted component")
        #     # log.info(normal_id2)
        #     v = np.delete(row, normal_id2)
        #     # log.info(v)
        # append to vert_x and vert_y
        vert_x.append(v[0])
        vert_y.append(v[1])
    # append the first vertex to the end of the list (circular)
    # if len(normal_id_equal[0]) == 1: # for 3 different normal components
    #     v = np.delete(vertcoord[0], normal_id_equal)
    # else: # normal has equal components
    #     normal_id2 = np.delete(normal_id_equal, 0)
    #     v = np.delete(vertcoord[0], normal_id2)
    v = np.take(vertcoord[0], normal_nig)
    # append to vert_x and vert_y
    vert_x.append(v[0])
    vert_y.append(v[1])
    # Transform in numpy array
    vert_x = np.array(vert_x) # doubles
    vert_y = np.array(vert_y) # doubles


    return vert_x, vert_y, normal_nig

def triangle_area(vertices):
    '''
    This function is used to calculate the area of a triagle
    Input: the vertices of a triangle
    Output: the area
    '''
    ab = vertices[1] - vertices[0]
    ab_norm = np.linalg.norm(ab)
    ac = vertices[2] - vertices[0]
    ac_norm = np.linalg.norm(ac)
    theta = np.arccos(np.dot(ab, ac)/(ab_norm * ac_norm))
    area_tri = 0.5 * ab_norm * ac_norm * np.sin(theta)
    return area_tri

def triangle_centroid(vertices):
    '''
    This function is used to calculate the centroid of a triagle
    Input: the vertices of a triangle
    Output: the centroid (1 x 3)
    '''
    return (vertices[0] + vertices[1] + vertices[2])/3

def total_area(planes):
    '''
    This function is used to calculate the total area of the room
    Input: a list of planes
    Output: the total area of the room
    '''
    total_area = 0.0
    for p in planes:
        total_area += p.area
    return total_area

def volume(planes):
    '''
    This function is used to calculate the volume of the room
    using scipy convexhull
    Input: a list of planes
    Output: the total area of the room
    '''
    vertex_list = []
    for p in planes:
        for v in p.vertices:
            vertex_list.append(v)
    volume = ConvexHull(vertex_list).volume
    return volume


# # Empty lists of x and y vertex coord
#     vert_x = []
#     vert_y = []
#     for row in vertcoord:
#         if len(normal_id_equal[0]) == 1: # for 3 different normal components
#             v = np.delete(row, normal_id_equal)
#             # log.info(v)
#         else: # normal has equal components
#             normal_id2 = np.delete(normal_id_equal, 0)
#             # log.info("non deleted component")
#             # log.info(normal_id2)
#             v = np.delete(row, normal_id2)
#             # log.info(v)
#         # append to vert_x and vert_y
#         vert_x.append(v[0])
#         vert_y.append(v[1])
#     # append the first vertex to the end of the list (circular)
#     if len(normal_id_equal[0]) == 1: # for 3 different normal components
#         v = np.delete(vertcoord[0], normal_id_equal)
#     else: # normal has equal components
#         normal_id2 = np.delete(normal_id_equal, 0)
#         v = np.delete(vertcoord[0], normal_id2)
#     # append to vert_x and vert_y
#     vert_x.append(v[0])
#     vert_y.append(v[1])
#     # Transform in numpy array
#     vert_x = np.array(vert_x) # doubles
#     vert_y = np.array(vert_y) # doubles