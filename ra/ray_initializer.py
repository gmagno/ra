import numpy as np
import ra_cpp

def ray_initializer(rays_vinit, N_max_ref):
        '''
        Initialize an array of rays with a bunch of planes and
        reflection points. This will allocate memory on the stack
        in order to computhe each ray history in the room
        '''
        rays = [] # An array of empty ray objects
        for ray in rays_vinit:
                planes = np.zeros(N_max_ref, dtype=int)
                reflection_points = np.zeros((N_max_ref, 3), dtype=float)
                ################### cpp ray class #################
                rays.append(ra_cpp.Raycpp(planes,
                        reflection_points)) # Append the ray object
        return rays