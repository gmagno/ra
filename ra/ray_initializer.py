import numpy as np
import ra_cpp

def ray_initializer(rays_dir, N_max_ref, trans_order, reccross):
        '''
        Initialize a std::vector of ray objects. Each ray object has
        the following properties:
        1: planes_hist - the history of planes indexes found during
                the ray travell in the room (1 x N_max_ref)
        2: refpts_hist - the history of reflection points found during
                the ray travell in the room (N_max_ref x 3 - floats)
        This will allocate memory on the stack in order to computhe
        each ray history in the room
        3: reccross - a std::vector of RecCross objects. Each RecCross object
                has the following properties: time_cross, rad_cross and
                ref_order. This data will be passed on to the sources
                objectes estabilishing the relation source-ray-receiver.
                time_cross, rad_cross and ref_order are allocated on the
                heap, since we don't know when each receiver will be crossed.
        '''
        rays = [] # An array of empty ray objects
        for jray in np.arange(rays_dir.Nrays):
                planes = np.zeros(N_max_ref, dtype=np.uint16)+65535 #npint16
                reflection_points = np.zeros((trans_order+2, 3), dtype=np.float32)
                ################### cpp ray class #################
                rays.append(ra_cpp.Raycpp(planes,
                        reflection_points, reccross)) # Append the ray object
        return rays