import codecs
import json
import time

import collada as co
import numpy as np
import toml
from tqdm import tqdm

import ra
from ra.ra import Simulation


#############
sim = Simulation(cfgfile='simulation.toml')

