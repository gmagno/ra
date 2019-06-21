import numpy as np
import toml
from ra.controlsair import load_cfg

def setup_receivers(config_file):
    '''
    Set up the sound sources
    '''
    receivers = [] # An array of empty receiver objects
    config = load_cfg(config_file) # toml file
    for r in config['sources']:
        coord = r['position']
        orientation = r['orientation']
        # Append the receiver object
        receivers.append(Receiver(coord, orientation)) 
    return receivers
            
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
        self.coord = np.array(coord)
        self.orientation = np.array(orientation)
    
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

    
   


