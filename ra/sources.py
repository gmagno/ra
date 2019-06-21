import numpy as np
import toml
from ra.controlsair import load_cfg

def setup_sources(config_file):
    '''
    Set up the sound sources
    '''
    sources = [] # An array of empty souce objects
    config = load_cfg(config_file) # toml file
    for s in config['sources']:
        coord = s['position']
        orientation = s['orientation']
        power_dB = s['power_dB']
        eq_dB = s['eq_dB']
        sources.append(Source(coord, orientation,
            power_dB, eq_dB)) # Append the source object
    return sources
            
class Source():
    '''
    A sound source class to initialize the following
    sound source properties:
    cood - 3D coordinates of a sound source
    orientation - where the source points to
    power_dB - the sound power in dB re 10e-12
    eq_dB - equalization of the sound source
    power_lin - the sound power in W

    For later we could implement: 
    directivity

    '''
    def __init__(self, coord, orientation, power_dB, eq_dB):
        self.coord = np.array(coord)
        self.orientation = np.array(orientation)
        self.power_dB = np.array(power_dB)
        self.eq_dB = np.array(eq_dB)
        self.power_lin = 10.0e-12 * 10**((self.power_dB + self.eq_dB) / 10.0)
    
# class Sources():
#     def __init__(self, config_file):
#         '''
#         Set up the sound sources
#         '''
#         config = load_cfg(config_file)
#         coord = []
#         orientation = []
#         power_dB = []
#         eq_dB = []
#         for s in config['sources']:
#             coord.append(s['position'])
#             orientation.append(s['orientation'])
#             power_dB.append(s['power_dB'])
#             eq_dB.append(s['eq_dB'])

#         self.coord = np.array(coord)
#         self.orientation = np.array(orientation)
#         self.power_dB = np.array(power_dB)
#         self.eq_dB = np.array(eq_dB)
#         self.power_lin = 10.0e-12 * 10**((self.power_dB + self.eq_dB) / 10.0)
