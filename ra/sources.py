import numpy as np
import toml
from ra.controlsair import load_cfg
import ra_cpp

def setup_sources(config_file, rays):
    '''
    Set up the sound sources
    Each sound source object has two main categories of data:
    A - sound source properties (given by user - read from toml):
    1:  coord - the 3D position of the receiver.
        orientation - the orientation of the receiver.
        power_dB - sound power in dB (len(contrlos.freq x 1)
        eq_dB - sound power equalization in dB (len(contrlos.freq x 1)
        power_lin - sound power in Watts (len(contrlos.freq x 1)
        delay - sound source delay [s].
    B - a std::vector of rays (objects). Each ray object contains:
        1: planes_hist - the history of planes indexes found during
            the ray travell in the room (1 x N_max_ref)
        2: refpts_hist - the history of reflection points found during
            the ray travell in the room (N_max_ref x 3 - floats) 
        3: a std::vector of reccross. Each recs object will contain 
            all source-ray-receiver relative data, such as:
                time_cross - the time instants for which a receiver is
                crossed for a given sound source and for a given ray.
                rad_cross - the receiver radius at the instant a receiver
                is crossed for a given sound source and for a given ray.
                ref_order - the reflection order at the instant a receiver
                is crossed for a given sound source and for a given ray.
    This way there is a dependence source-ray-receiver
    '''
    sources = [] # An array of empty souce objects
    config = load_cfg(config_file) # toml file
    for s in config['sources']:
        coord = np.array(s['position'], dtype=np.float32)
        orientation = np.array(s['orientation'], dtype=np.float32)
        power_dB = np.array(s['power_dB'], dtype=np.float32)
        eq_dB = np.array(s['eq_dB'], dtype=np.float32)
        power_lin = 10.0e-12 * 10**((power_dB + eq_dB) / 10.0)
        delay = s['delay'] / 1000
        ################### cpp source class #################
        sources.append(ra_cpp.Sourcecpp(coord, orientation,
            power_dB, eq_dB, power_lin, delay, rays)) # Append the source object
        # sources.append([ra_cpp.Sourcecpp(coord, orientation,
        #     power_dB, eq_dB, power_lin, delay),
        #     rays]) # Append the source object
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