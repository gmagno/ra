import numpy as np
from scipy.spatial import ConvexHull
import toml
import collada as co
from ra.controlsair import load_cfg
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import scipy.io as spio
import ra_cpp

class GeometryMat():
    def __init__(self, config_file, alpha, s):
        '''
        Set up the room geometry from the .mat file
        '''
        config = load_cfg(config_file)
        # print(config['geometry']['room'])
        # print(type('ODEON_Ex_geometry.mat'))
        mat = spio.loadmat(config['geometry']['room'],
            struct_as_record = True)

        vertcoord = np.array(mat['geometry']['vertcoord'][0][0])
        self.planes = []
        planes = mat['geometry']['plane'][0][0][0]
        for jp, p in enumerate(planes):
            name = 'nameless matlab plane'
            vertices = []
            for v in p[0][0]:
                vertices.append(vertcoord[v-1])
            vertices  = np.array(vertices)
            normal = np.float32(p[1][0])
            vert_x, vert_y, normal_nig = vert_2d(normal, vertices)
            area = np.float64(p[2][0])
            centroid = np.float32(p[3][0])
            alpha_v = np.float32(alpha[jp])
            ################### cpp plane class #################
            # print("Plane area in Py before c++: {}.".format(area))
            # print(type(area))
            plane = ra_cpp.PlaneMat(name, False, vertices, normal,
                vert_x, vert_y, normal_nig, area, centroid,
                alpha_v, s[jp])
            # print(plane.get_area())
            # print(plane.get_pname())
            ###################################################
            # plane = PyPlaneMat(name, vertices, normal, area,
            #     centroid, alpha[jp], s[jp])
            self.planes.append(plane)
        self.total_area = np.array(mat['geometry']['TotalArea'])
        self.volume = np.array(mat['geometry']['Volume'])
        # pet = ra_cpp.Pet('pluto', 5)
        # print(pet.get_name())

    def plot_mat_room(self, normals='off'):
        '''
        a simple plot of the room - not redered
        '''
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        
        for plane in self.planes:
                ax.scatter(plane.vertices[:,0], plane.vertices[:,1],
                    plane.vertices[:,2], color='blue')
                
                verts = [list(zip(plane.vertices[:,0], 
                    plane.vertices[:,1], plane.vertices[:,2]))]
                
                collection = Poly3DCollection(verts,
                    linewidths=1, alpha=0.5, edgecolor = 'gray')
                face_color = 'silver' # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
                collection.set_facecolor(face_color)
                ax.add_collection3d(collection)

                if normals == 'on':
                    ax.quiver(plane.centroid[0], plane.centroid[1], 
                    plane.centroid[2], plane.normal[0],
                    plane.normal[1], plane.normal[2],
                    length=1, color = 'red', normalize=True)
                    

        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show()    

class PyPlaneMat():

    '''
    A class to define a single plane object with the following att:
    name = Name of the object. Default = 'none'
    vertices = the list of 3, 3D vertices - from .dae
    normal = the normal of the plane - from .dae
    '''
    def __init__(self, name, vertices, normal, area, centroid, alpha, s):
        self.name = name
        self.bbox = False  # by default a plane is part of the room geometry
        self.vertices = np.array(vertices, np.float32)
        self.normal = np.float32(normal)
        # For point in polygon test we can do it in 2D
        # It is better to return a list of 2D vertexes once and for all   
        self.vert_x, self.vert_y = vert_2d(self.normal, self.vertices)
        # Calculate the area of each polygon
        self.area = area
        # Calculate the centroiud of a polygon
        self.centroid = np.float32(centroid)
        # The acoustical properties of the plane
        self.s = s
        self.alpha = np.array(alpha, np.float32)

class Geometry():
    def __init__(self, config_file):
        '''
        Set up the room geometry from the .dae file
        '''
        config = load_cfg(config_file)          # config. file
        daepath=config['geometry']['room']      # path to .dae

        self.planes = []    # A list of planes (object with attributes)
        mesh = co.Collada(daepath)
        
        for obj in mesh.scene.objects('geometry'): #loop every obj
            for triset in obj.primitives():
                # First if excludes the triangles
                if type(triset) != co.triangleset.BoundTriangleSet:
                    print('Warning: non-supported primitive ignored!')
                    continue
                # Loop trhough all triangles
                for i, tri in enumerate(triset):
                    # Define a single plane object  
                    plane = Plane(
                        name='{}-{}'.format(obj.original.name, i),
                        vertices=tri.vertices,
                        normal=tri.normals[0] / np.linalg.norm(tri.normals[0])
                    )

                    # Append the plane object to a list of planes
                    self.planes.append(plane)
        self.total_area = total_area(self.planes)
        self.volume = volume(self.planes)

    def plot_dae_room(self, normals='off'):
        '''
        a simple plot of the room - not redered
        '''
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        
        for plane in self.planes:
                ax.scatter(plane.vertices[:,0], plane.vertices[:,1],
                    plane.vertices[:,2], color='blue')
                
                verts = [list(zip(plane.vertices[:,0], 
                    plane.vertices[:,1], plane.vertices[:,2]))]
                
                collection = Poly3DCollection(verts,
                    linewidths=1, alpha=0.5, edgecolor = 'gray')
                face_color = 'silver' # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
                collection.set_facecolor(face_color)
                ax.add_collection3d(collection)

                if normals == 'on':
                    ax.quiver(plane.centroid[0], plane.centroid[1], 
                    plane.centroid[2], plane.normal[0],
                    plane.normal[1], plane.normal[2],
                    length=1, color = 'red', normalize=True)
                    

        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show()


class Plane():
    '''
    A class to define a single plane object with the following att:
    name = Name of the object. Default = 'none'
    vertices = the list of 3, 3D vertices - from .dae
    normal = the normal of the plane - from .dae
    '''
    def __init__(self, name, vertices, normal):
        self.name = name
        self.bbox = False  # by default a plane is part of the room geometry
        self.vertices = np.array(vertices, np.float32)
        self.normal = np.float32(normal)
        # For point in polygon test we can do it in 2D
        # It is better to return a list of 2D vertexes once and for all   
        self.vert_x, self.vert_y = vert_2d(self.normal, self.vertices)
        # Calculate the area of each polygon
        self.area = triangle_area(self.vertices)
        # Calculate the centroiud of a polygon
        self.centroid = triangle_centroid(self.vertices)


def vert_2d(normal, vertcoord):
    '''
    Function to transform the 3D plane to 2D.
    Input: normal of the plane
    3D vertex coordinates of the plane (array of 1x3 arrays)
    Output: vert_x: a numpy array of x-coordinates of vertexes
            vert_y: a numpy array of y-coordinates of vertexes 
    '''
    # Find biggest component of the normal - component to ignore
    normal_abs = np.absolute(normal)
    normal_id = np.where(normal_abs == normal_abs.max())
    normal_nig = np.where(normal_abs != normal_abs.max())

    vert_x = []
    vert_y = []
    for row in vertcoord:
        # v = np.delete(row, normal_id)
        if len(normal_id[0]) == 1:
            v = np.delete(row, normal_id)
        else:
            normal_id2 = np.delete(normal_id, 0)
            v = np.delete(row, normal_id2)

        vert_x.append(v[0])
        vert_y.append(v[1])

    # append the first vertex to the end of the list (circular)
    if len(normal_id[0]) == 1:
        v = np.delete(vertcoord[0], normal_id)
    else:
        normal_id2 = np.delete(normal_id, 0)
        v = np.delete(vertcoord[0], normal_id2)
    vert_x.append(v[0])
    vert_y.append(v[1])

    # Transform in numpy array
    vert_x = np.array(vert_x)
    vert_y = np.array(vert_y)
    normal_nig = np.intc(normal_nig[0])
    return vert_x, vert_y, normal_nig

def triangle_area(vertices):
    ab = vertices[1] - vertices[0]
    ab_norm = np.linalg.norm(ab)
    ac = vertices[2] - vertices[0]
    ac_norm = np.linalg.norm(ac)
    theta = np.arccos(np.dot(ab, ac)/(ab_norm * ac_norm))
    area_tri = 0.5 * ab_norm * ac_norm * np.sin(theta)
    return area_tri

def triangle_centroid(vertices):
    return (vertices[0] + vertices[1] + vertices[2])/3

def total_area(planes):
    total_area = 0.0
    for p in planes:
        total_area += p.area
    return total_area

def volume(planes):
    vertex_list = [] 
    for p in planes:
        for v in p.vertices:
            vertex_list.append(v)
    
    volume = ConvexHull(vertex_list).volume
    return volume