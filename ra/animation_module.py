import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
import ra_cpp
from controlsair import load_sim


class BilliardPts(object):
    """ A class to run some animations of billiards in a room
    """
    def __init__(self, source, geometry, ds = 0.5, n_billiards = 50, fps = 20, figsize = (7,5)):
        """ Init animation object with source and geometry

        Inputs :
        ds : float
            space between two consecutive billiards [m]
        c0 : float
            sound speed
        n_billiards : int
            number of billiard points emanating from source
        """
        self.source = source
        self.geometry = geometry
        self.ds = ds
        self.n_billiards = int(n_billiards)
        self.fig = plt.figure(figsize = figsize)
        self.ax = self.fig.gca(projection='3d')
        self.fps = fps
        self.color_dict = np.array(['blue', 'green','brown', 'darkmagenta',
            'goldenrod', 'lightcoral', 'siena', 'royalblue', 'olive'])#{0:'blue', 1:'green', 2:'brown', 3:'darkmagenta',
            # 4:'goldenrod', 5:'lightcoral', 6:'siena', 7:'royalblue', 8:'olive'}

    def line_pts(self, r0, rp):
        """ Calculate a set of points on a ray segment

        Inputs :
        r0 : 1d npArray
            Initial point of a ray segment
        rp : 1d npArray
            End point of a ray segment
        """
        dist = np.linalg.norm(rp-r0) # total distance between pts
        v = (rp-r0)/dist # unitary direction vector
        Npts = np.ceil(dist/self.ds) # number of pts in the segment
        lam_seg = dist/Npts # calculated distance to move billiard
        nn = np.arange(1, Npts)
        # print(" dist {}, v {}, Npts {}, lam_seg {}, nn {}".format(dist, v,Npts,lam_seg, nn))
        rn = np.reshape(r0, (1,3)) + lam_seg * np.reshape(nn,(len(nn),1)) @ np.reshape(v, (1,3))
        return rn

    def ray_pts(self, jray = 0):
        """ Calculate a set of points on all ray segments
        """
        # Initiate empty list
        ray_coord_list = []
        ro_list = []
        # discretize first segment (source to first reflection point)
        rn = self.line_pts(self.source.coord, self.source.rays[jray].refpts_hist[0,:])
        ray_coord_list.append(rn)
        ro_list.append(np.zeros(rn.shape[0]))
        # ncoords = rn.shape[0]
        nsegs = self.source.rays[jray].refpts_hist.shape[0]
        for jseg in np.arange(1, nsegs):
            # discretize remaining segments
            rn = self.line_pts(self.source.rays[jray].refpts_hist[jseg-1,:],
                self.source.rays[jray].refpts_hist[jseg,:])
            # ncoords += rn.shape[0]
            ray_coord_list.append(rn)
            try:
                ro_list.append(jseg*np.ones(rn.shape[0]))
            except:
                ro_list.append(8*np.ones(rn.shape[0]))
        # stack everything
        ray_coords = np.vstack(np.array(ray_coord_list[:]))
        ro = np.hstack(np.array(ro_list[:]))
        ray_coords = np.vstack((self.source.coord, ray_coords))
        ro = np.hstack((0, ro))
        return ray_coords, ro

    def calc_billiardpts(self, seed = 0):
        """ Calculate billiard points at each animation step
        """
        # sort rays to billiard
        print("Assembling billiards...")
        np.random.seed(seed)
        rays2plot = np.random.randint(0, len(self.source.rays), size=self.n_billiards)
        # empty list
        ray_coord_list = []
        ro_list = []
        for jray in rays2plot:
            ray_cds, ro_cds = self.ray_pts(jray = jray)
            ray_coord_list.append(ray_cds)
            ro_list.append(ro_cds)
        # print(ray_coord_list[0].shape)
        # print(ro_list[0].shape)
        # print(ray_coord_list[1].shape)
        # print(ro_list[1])
        # discover max order
        order = []
        for raycl in ray_coord_list:
            order.append(raycl.shape[0])
        max_order = np.amax(np.array(order))
        # organize it
        self.ray_list_po = []
        self.ro_list_po = []
        for jp in np.arange(max_order):
            coord_list = []
            ro_int_list = []
            for jray, raycl in enumerate(ray_coord_list):
                if jp < raycl.shape[0]:
                    coord_list.append(raycl[jp,:])
                    ro_int_list.append(ro_list[jray][jp])
            self.ray_list_po.append(np.array(coord_list))
            self.ro_list_po.append(np.array(ro_int_list, dtype=int))
        # print(self.ray_list_po[0].shape)
        # print(self.ray_list_po[1].shape)
        # print(self.ray_list_po[20].shape)
        # print(self.ro_list_po[0].shape)
        # print(self.ro_list_po[1].shape)
        # print(self.color_dict[self.ro_list_po[20]])
        # return ray_coord_list, ray_list_po

    def plot_room(self):
        """a simple plot of the room and source"""
        # First plot the room
        for plane in self.geometry.planes:
            # vertexes plot
            self.ax.scatter(plane.vertices[:,0], plane.vertices[:,1],
                plane.vertices[:,2], color='grey', s=1)
            # patch plot
            verts = [list(zip(plane.vertices[:,0],
                plane.vertices[:,1], plane.vertices[:,2]))]
            collection = Poly3DCollection(verts,
                linewidths=1, alpha=0.3, edgecolor = 'gray')
            face_color = 'silver' # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
            collection.set_facecolor(face_color)
            self.ax.add_collection3d(collection)
        # plot the sound source
        self.ax.scatter(self.source.coord[0], self.source.coord[1], self.source.coord[2],
            color='red',  marker = "o", s=200)
        self.ax.set_xlabel(r'$x$ [m]')
        self.ax.set_ylabel(r'$y$ [m]')
        self.ax.set_zlabel(r'$z$ [m]')
        self.ax.set_axis_off()
        plt.tight_layout()

    def init_anim(self):
        """ initialization function: plot the background of each frame
        """
        self.ax.scatter([], [], [], color='blue', s=5, alpha = 0.5)

    def animate(self, i):
        """ Animation function.  This is called sequentially
        """
        self.ax.clear()
        self.plot_room()

        # self.ax.scatter(self.ray_list_po[i][:,0], self.ray_list_po[i][:,1], self.ray_list_po[i][:,2], 
        #     color='blue', s=5, alpha = 0.5)

        colors = self.color_dict[np.array(self.ro_list_po[i])]
        self.ax.scatter(self.ray_list_po[i][:,0], self.ray_list_po[i][:,1], self.ray_list_po[i][:,2], 
            color=colors, s=5, alpha = 0.5)

    def trace_billiards(self, seed = 0):
        self.calc_billiardpts(seed = seed)
        self.plot_room()
        # print("color: {}".format(self.ro_list_po[0]))
        self.ax.scatter([], [], [], color='blue', s=5, alpha = 0.5)
        self.anim = animation.FuncAnimation(self.fig, self.animate, frames = len(self.ray_list_po),
            init_func=self.init_anim,  repeat=False, interval = 25)

    def save_animation(self, path='', filename = '', target_time = 3):
        fps = int(len(self.ray_list_po)/target_time)
        path_file = path + filename + '.gif'
        self.anim.save(path_file , writer='imagemagick', fps=fps)

def billiard(source, geometry):
    global sc, ax, fig, ray_coords, ray_list_po, ray_coord_list, markersize
    global src, geo
    markersize = 5
    ds = 0.5
    dt = 1/30
    c0 = 343
    nrays = 50
    src = source
    geo = geometry
    ray_coords = ray_pts(source, jray = 0, ds = ds, dt = dt, c0 = c0)
    
    ray_coord_list, ray_list_po = calc_billiardpts(source, ds = ds, dt = dt, c0 = c0, nrays = nrays, seed = 0)
    fig = plt.figure(figsize = (7,5))
    ax = fig.gca(projection='3d')
    ### Animate
    plot_room(source.coord, geometry.planes, figsize = (20,16))
    sc = ax.scatter([], [], [], color='blue', s=5, alpha = 0.5)

    # sc, = ax.plot([], [], [], color='blue', marker = 'o', markersize=markersize, alpha = 0.5)
    ray_coords = ray_pts(source, jray = 0, ds = ds, dt = dt, c0 = c0)
    anim = animation.FuncAnimation(fig, animate, frames = 150,
        init_func=init,  repeat=False, interval = 53)
    anim.save('/home/eric/dev/ra/data/legacy/odeon_ex/room_ex.gif', writer='imagemagick', fps=15)
    # anim = animation.FuncAnimation(fig, animate, frames = ray_coords.shape[0],
    #     init_func=init,  repeat=False, interval = 53, blit=True)

    # anim = animation.FuncAnimation(fig, animate, frames = ray_coord_list[0].shape[0],
    #     init_func=init,  repeat=False, interval = 53, blit=True)
    plt.show()
    #### End animation
    # rn = line_pts(source.coord, source.rays[0].refpts_hist[0,:])
    



def init():
    """ initialization function: plot the background of each frame
    """
    # sc.set_data([], [], [])
    sc = ax.scatter([], [], [], color='blue', s=5, alpha = 0.5)
    # sc, = ax.plot([], [], [], color='blue', marker = 'o', markersize=markersize, alpha = 0.5)
    return sc

def animate(i):
    """ Animation function.  This is called sequentially
    """
    # sc = ax.scatter(ray_coords[i,0], ray_coords[i,1], ray_coords[i,2], 
    #     color='blue', s=10, alpha = 0.5)
    ax.clear()
    plot_room(src.coord, geo.planes, figsize = (20,16))

    # ax, fig = plot_room(src.coord, geo.planes, figsize = (20,16))
    sc = ax.scatter(ray_list_po[i][:,0], ray_list_po[i][:,1], ray_list_po[i][:,2], 
        color='blue', s=5, alpha = 0.5)
    # sc = ax.scatter(ray_list_po[i-1][:,0], ray_list_po[i-1][:,1], ray_list_po[i-1][:,2], 
    #     color='white', s=5, alpha = 0.5)
    # sc.remove()
    
    
    # sc.set_offsets([])
    # sc = ax.scatter([], [], [], color='white', s=5, alpha = 0.3)
    # sc, = ax.plot(ray_coords[i:i+1,0], ray_coords[i:i+1,1], ray_coords[i:i+1,2],
    #     color='blue', marker = 'o', markersize=markersize, alpha = 0.5)

    # sc, = ax.plot(ray_coord_list[0][i:i+1,0], ray_coord_list[0][i:i+1,1], ray_coord_list[0][i:i+1,2],
    #     color='blue', marker = 'o', markersize=markersize, alpha = 0.5)
    # pt1 = ray_list_po[i][0,:]
    # pt2 = ray_list_po[i+1][0,:]
    # for jp in np.arange(ray_list_po[i][:,:].shape[0]):
    #     sc, = ax.plot([ray_list_po[i][jp,0]], [ray_list_po[i][jp,1]], [ray_list_po[i][jp,2]],
    #         color='blue', marker = 'o', markersize=markersize, alpha = 0.5)
    return sc

def calc_billiardpts(source, ds = 0.25, dt = 1/30, c0 = 343, nrays = 10, seed = 0):
    # sort rays to billiard
    np.random.seed(seed)
    rays2plot = np.random.randint(0, len(source.rays), size=nrays)
    ray_coord_list = []
    for jray in rays2plot:
        ray_cds = ray_pts(source, jray = jray, ds = ds, dt = dt, c0 = c0)
        ray_coord_list.append(ray_cds)
    # discover max order
    order = []
    for raycl in ray_coord_list:
        order.append(raycl.shape[0])
    max_order = np.amax(np.array(order))
    # organize it
    ray_list_po = []
    for jp in np.arange(max_order):
        coord_list = []
        for raycl in ray_coord_list:
            if jp < raycl.shape[0]:
                coord_list.append(raycl[jp,:])
        ray_list_po.append(np.array(coord_list))
    # print(ray_list_po[0].shape)
    # print(ray_list_po[1].shape)
    # print(ray_list_po[2].shape)
    # print(ray_list_po[64].shape)
    # print(ray_list_po[79].shape)
    # print(ray_list_po[100].shape)
    return ray_coord_list, ray_list_po
    # ray_coords = np.vstack(np.array(ray_coord_list[:]))
    # print(ra)

def ray_pts(source, jray = 0, ds = 0.25, dt = 1/30, c0 = 343):
    """ Calculate a set of points on all ray segments
    """
    ray_coord_list = []
    rn = line_pts(source.coord, source.rays[jray].refpts_hist[0,:])
    ncoords = rn.shape[0]
    ray_coord_list.append(rn)
    nsegs = source.rays[jray].refpts_hist.shape[0]
    for jseg in np.arange(1, nsegs):
        rn = line_pts(source.rays[jray].refpts_hist[jseg-1,:],
            source.rays[jray].refpts_hist[jseg,:], ds = ds, dt = dt, c0 = c0)
        ncoords += rn.shape[0]
        ray_coord_list.append(rn)
    ray_coords = np.vstack(np.array(ray_coord_list[:]))
    ray_coords = np.vstack((source.coord, ray_coords))
    # ax.scatter(ray_coords[:,0], ray_coords[:,1], ray_coords[:,2], color='blue', s=10)
    return ray_coords


def line_pts(r0, rp, ds = 0.25, dt = 1/30, c0 = 343):
    """ Calculate a set of points on a ray segment
    """
    # lam = dt*c0 # target distance to move the billiard
    dist = np.linalg.norm(rp-r0) # total distance between pts
    v = (rp-r0)/dist # unitary direction vector
    Npts = np.ceil(dist/ds) # number of pts in the segment
    lam_seg = dist/Npts # calculated distance to move billiard
    nn = np.arange(1, Npts)
    # print(" dist {}, v {}, Npts {}, lam_seg {}, nn {}".format(dist, v,Npts,lam_seg, nn))
    rn = np.reshape(r0, (1,3)) + lam_seg * np.reshape(nn,(len(nn),1)) @ np.reshape(v, (1,3))
    return rn

def plot_room(sourcecoord, planes, figsize = (7,5)):
        """a simple plot of the room and source"""
        # fig = plt.figure(figsize = (7,5))
        # ax = fig.gca(projection='3d')
        # First plot the room
        for plane in planes:
            # vertexes plot
            ax.scatter(plane.vertices[:,0], plane.vertices[:,1],
                plane.vertices[:,2], color='grey', s=1)
            # patch plot
            verts = [list(zip(plane.vertices[:,0],
                plane.vertices[:,1], plane.vertices[:,2]))]
            collection = Poly3DCollection(verts,
                linewidths=1, alpha=0.3, edgecolor = 'gray')
            face_color = 'silver' # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
            collection.set_facecolor(face_color)
            ax.add_collection3d(collection)
        # plot the sound source
        ax.scatter(sourcecoord[0], sourcecoord[1], sourcecoord[2],
            color='red',  marker = "o", s=200)
        # plot receivers
        # for rec in receivers:
        #     ax.scatter(rec.coord[0], rec.coord[1],
        #         rec.coord[2], color='blue', s=100)

        # # plot the ray path
        # ray_vec = raypath[0,:]-sourcecoord
        # arrow_length = np.linalg.norm(ray_vec)
        # ax.quiver(sourcecoord[0], sourcecoord[1], sourcecoord[2],
        #         ray_vec[0], ray_vec[1], ray_vec[2],
        #         arrow_length_ratio = 0.006 * arrow_length)
        # N_max_ref = len(raypath)
        # for jray in np.arange(N_max_ref-1):
        #     ray_origin = raypath[jray]
        #     ray_vec = raypath[jray+1]-raypath[jray]
        #     arrow_length = np.linalg.norm(ray_vec)
        #     ax.quiver(ray_origin[0], ray_origin[1], ray_origin[2],
        #         ray_vec[0], ray_vec[1], ray_vec[2],
        #         arrow_length_ratio = 0.006 * arrow_length)

        #     ax.scatter(raypath[jray,0], raypath[jray,1],
        #         raypath[jray,2], color='red', marker = "+")
        # set axis labels
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        # return ax, fig
