import numpy as np
import toml
from ra.controlsair import load_cfg
import ra_cpp

def setup_sources(config_file):
    '''
    Set up the sound sources
    '''
    sources = [] # An array of empty souce objects
    config = load_cfg(config_file) # toml file
    for s in config['sources']:
        coord = np.array(s['position'])
        orientation = np.array(s['orientation'])
        power_dB = np.array(s['power_dB'])
        eq_dB = np.array(s['eq_dB'])
        power_lin = 10.0e-12 * 10**((power_dB + eq_dB) / 10.0)
        delay = s['delay'] / 1000
        ################### cpp source class #################
        sources.append(ra_cpp.Sourcecpp(coord, orientation,
            power_dB, eq_dB, power_lin, delay)) # Append the source object
        ################### py source class ################
        # sources.append(Source(coord, orientation,
        #     power_dB, eq_dB, power_lin, delay)) # Append the source object
    return sources
# class Souces from python side
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
    def __init__(self, coord, orientation, power_dB, eq_dB, power_lin, delay):
        self.coord = coord
        self.orientation = orientation
        self.power_dB = power_dB
        self.eq_dB = eq_dB
        self.power_lin = power_lin
        self.delay = delay