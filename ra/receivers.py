import numpy as np
import toml
import ra_cpp


def setup_receivers(receivers_cfg):
    '''
    Set up the receivers. There are two arrays of receivers.
    1: receivers - contains a receiver object with the properties:
        coord - the 3D position of the receiver.
        orientation - the orientation of the receiver.
    2: reccross - this object will contain all source-ray-receiver
        relative data, such as:
        time_cross - the time instants for which a receiver is crossed
        for a given sound source and for a given ray.
        rad_cross - the receiver radius at the instant a receiver is crossed
        for a given sound source and for a given ray.
        ref_order - the reflection order at the instant a receiver is crossed
        for a given sound source and for a given ray.
        An std::vector of reccross objects will be passed to each ray
        object, generating an std::vector of rays. These rays will be
        passed to each source object. This will generate the dependence
        source-ray-receiver
    '''
    receivers = [] # An array of empty receiver objects
    reccross = [] # An array of empty reccross data objects
    reccrossdir = [] # An array of empty reccrossdir data objects
    # To process reccross
    # time_cross = np.zeros(1, dtype = np.float32)
    # rad_cross = np.zeros(1, dtype = np.float32)
    # ref_order = np.zeros(1, dtype = np.uint16)
    for r in receivers_cfg:
        coord = np.array(r['position'], dtype=np.float32)
        orientation = np.array(r['orientation'], dtype=np.float32)
        ################### cpp receiver class #################
        receivers.append(ra_cpp.Receivercpp(coord, orientation)) # Append the receiver object
        reccross.append(ra_cpp.RecCrosscpp([], [], [], [])) # Append the reccross object
        reccrossdir.append(ra_cpp.RecCrossDircpp(0, 0.0, 0, 0.0))
        ################### py source class ################
        # receivers.append(Receiver(coord, orientation))
    return receivers, reccross, reccrossdir

# class Receiver from python side
class Receiver():
    '''
    A receiver class to initialize the following
    receiver properties:
    cood - 3D coordinates of a sound source
    orientation - where the source points to
    For later we could implement:
    point to a given sound source
    '''
    def __init__(self, coord, orientation):
        self.coord = coord
        self.orientation = orientation
    # point receiver to a given sound source
    def point_to_source(self, sourceid = 0):
        '''
        Point the receiver towards a sound source
        '''
        pass

# class Receivers():
#     def __init__(self, config_file):
#         '''
#         Set up the receivers
#         '''
#         config = load_cfg(config_file)
#         coord = []
#         orientation = []
#         for r in config['receivers']:
#             coord.append(r['position'])
#             orientation.append(r['orientation'])
#         self.coord = np.array(coord)
#         self.orientation = np.array(orientation)

