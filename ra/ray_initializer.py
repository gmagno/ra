import numpy as np
import ra_cpp

def ray_initializer(rays_dir, N_max_ref):
        '''
        Initialize an array of rays with a bunch of planes and
        reflection points. This will allocate memory on the stack
        in order to computhe each ray history in the room
        '''
        # print(rays_dir.Nrays)
        # a = np.arange(rays_dir.Nrays)
        # print(a)
        rays = [] # An array of empty ray objects
        for jray in np.arange(rays_dir.Nrays):
                planes = np.zeros(N_max_ref, dtype=int)-10
                reflection_points = np.zeros((N_max_ref, 3), dtype=float)
                ################### cpp ray class #################
                rays.append(ra_cpp.Raycpp(planes,
                        reflection_points)) # Append the ray object
        return rays