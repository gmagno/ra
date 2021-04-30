import pickle
import numpy as np
import matplotlib.pyplot as plt
import ra_cpp
from controlsair import load_sim
from animation_module import billiard, BilliardPts

#%% Load
# path = '/home/eric/dev/ra/data/legacy/odeon_ex/'
# pkl_fname_res = 'odeon_ex_testpickle'        # simulation results name

# path = '/home/eric/research/ray_tracing/trem_example/'
# pkl_fname_res = 'ex_testpickle'        # simulation results name

# path = '/home/eric/dev/ra/data/legacy/elmia/'
# pkl_fname_res = 'elmia_odeon_400k'

path = '/home/eric/research/ray_tracing/ptbst_ph2_odeon/'
pkl_fname_res = 'ptbst_ph2_open'

controls, air, rays_i, geometry,\
    stats_theory, sources, receivers,\
    s_reflecto_par, stats_analysis = load_sim(path=path, fname=pkl_fname_res)

#%% 
# geometry.plot_raypath(sources[0].coord, sources[0].rays[0].refpts_hist, receivers)

# billiard(sources[0], geometry)
bill = BilliardPts(sources[0], geometry, n_billiards = 4000, ds = 0.5 , figsize=(16,9))
# bill.calc_billiardpts()
# bill.plot_room()

bill.trace_billiards()
bill.save_animation(path = path, filename=pkl_fname_res+'_2gif', target_time = 9)
# plt.show()