import pickle
import numpy as np
import matplotlib.pyplot as plt
from ra.results import SRStats

# path = 'data/legacy/odeon_ex/'          # room folder
# pkl_fname_res = 'odeon_ex'              # simulation results name
# path = 'data/legacy/ptb_studio_ph1/'    # room folder
# pkl_fname_res = 'ptb_studio_ph1'        # simulation results name
path = 'data/legacy/ptb_studio_ph3/'    # room folder
# pkl_fname_res = 'ptb_studio_ph2_open'        # simulation results name
pkl_fname_res = 'ptb_studio_ph3_open'        # simulation results name
tml_name_cfg = 'simulation.toml'        # toml configuration file
# tml_name_mat = 'surface_mat_id.toml'    # toml material file



with open(path+pkl_fname_res+'.pkl', 'rb') as input:
    res_stat = pickle.load(input)
    sou = pickle.load(input)
    stats = pickle.load(input)

# stats = SRStats(sou)
# stats.plot_edt_f(plotsr = False)
# stats.plot_t20_f(plotsr = True)
stats.plot_t30_f(plotsr = True)
# stats.plot_c80_f(plotsr = True)
# stats.plot_d50_f(plotsr = True)
# stats.plot_ts_f(plotsr = True)
# stats.plot_g_f(plotsr = True)
# stats.plot_lf_f(plotsr = True)
# stats.plot_lfc_f(plotsr = True)
plt.show()

# res_stat.plot_t60()
# sou[0].plot
# sou[0].plot_t30()
# sou[0].plot_c80()
# sou[1].plot_c80()