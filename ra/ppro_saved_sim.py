import pickle
import numpy as np
import matplotlib.pyplot as plt
import ra_cpp
from controlsair import load_sim

#%% Load
path = '/home/eric/dev/ra/data/legacy/ptb_studio_ph1/'
pkl_fname_res = 'ptb_ph1'        # simulation results name
controls, air, rays_i, geometry,\
    stats_theory, sources, receivers,\
    s_reflecto_par, stats_analysis = load_sim(path=path, fname=pkl_fname_res)

print(geometry.volume)
#%% Test some plots
# print(stats_theory.alphas_mtx.shape)
# sources = ra_cpp._intensity_main(controls.rec_radius_init,
#     sources, air.c0, air.m, stats_theory.alphas_mtx)
# s_reflecto_par[0].plot_t30()

# stats_theory.plot_t60()
# geometry.plot_mat_room(normals = 'on')
# print(sources[0].rays[0].planes_hist)
# print(sources[0].rays[10].refpts_hist)
# print(sources[0].rays[1].recs[2].time_cross)
# print(sources[0].reccrossdir[0].time_dir)
# geometry.plot_raypath(sources[0].coord, sources[0].rays[0].refpts_hist,  # <-- sources[0].rays[0].refpts_hist
#     receivers)
# print(s_reflecto_par[0].rec[0].T30)
# print(s_reflecto_par[1])
#%%
SMALL_SIZE = 12
BIGGER_SIZE = 13
#plt.rcParams.update({'font.size': 10})
plt.rcParams.update({'font.family': 'serif'})
plt.rc('legend', fontsize=SMALL_SIZE)
#plt.rc('title', fontsize=SMALL_SIZE)
plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('figure', titlesize=BIGGER_SIZE)

s_reflecto_par[0].plot_single_reflecrogram(band = 4, jrec = 2)

freq_ticks = []
for f in controls.freq:
    freq_ticks.append(str(f))

fig = plt.figure()
fig.canvas.set_window_title("EDT vs. freq")
for js in np.arange(2):
    for jr in np.arange(3):
        legend = 'S: ' + str(js+1) + ', R: ' + str(jr+1)
        plt.plot(controls.freq[1:-1], s_reflecto_par[js].rec[jr].T30[1:-1], label = legend)
plt.plot(controls.freq[1:-1], stats_theory.t60_s[1:-1], '-k', linewidth = 2,label = 'Sabine')
plt.grid(linestyle = '--')
plt.legend(loc = 'best')
plt.xscale('log')
# plt.title(r'$T_{30}$ vs. freq.')
plt.xticks(controls.freq[1:-1], freq_ticks[1:-1])
plt.xlabel('Frequency [Hz]')
plt.ylabel(r'$T_{30}$ [s]')
plt.ylim((0, 2.5))
plt.show()

print('difference {}'.format(stats_theory.t60_s[1:-1]-s_reflecto_par[js].rec[jr].T30[1:-1]))