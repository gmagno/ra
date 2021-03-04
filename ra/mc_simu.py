import pickle
import numpy as np
import matplotlib.pyplot as plt
import ra_cpp
from controlsair import load_sim
from monte_carlo import MCRoomAcoustics

#%% Load
path = '/home/eric/dev/ra/data/legacy/odeon_ex/'
pkl_fname_res = 'odeon_ex_testpickle'        # simulation results name
controls, air, rays_i, geometry,\
    stats_theory, sources, receivers,\
    s_reflecto_par, stats_analysis = load_sim(path=path, fname=pkl_fname_res)

#%% Mc sim
mc = MCRoomAcoustics(controls = controls, air = air,
    geometry = geometry, stats_theory = stats_theory, sources = sources, Nmc = 50)
mc.create_abs_pop(rel_std=0.1)
mc.plot_absorption(desired_plane=1)
mc.run_mc()
mc.plot_t60_sabine()
# mc.plot_histogram(desired_plane=1, rel_hist=True)
plt.show()

