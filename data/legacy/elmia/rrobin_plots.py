import pickle
import numpy as np
import matplotlib.pyplot as plt
from ra.results import SRStats
from data.legacy.ptb_studio_ph3.ppro_rrobin_classes import ParRoundRobin, SouRoundRobin, RecRoundRobin

# Load round robin data
pkl_fname = 'data/legacy/elmia/rrobin2_elmia.pkl'
# pkl_fname = 'data/legacy/ptb_studio_ph3/rrobin3_par_close.pkl'
with open(pkl_fname, 'rb') as input:
    participant = pickle.load(input)

# Load TREM data
path = 'data/legacy/elmia/'    # room folder
pkl_fname_res = 'elmia_odeon'        # simulation results name
with open(path+pkl_fname_res+'.pkl', 'rb') as input:
    res_stat = pickle.load(input)
    sou = pickle.load(input)
    stats = pickle.load(input)

sou[0].plot_single_reflecrogram(band = 4, jrec = 0)

def plot_vs_freq(sou, participant, js, jrec, softname, par, y_limits):
    trem_parameter = getattr(sou[0].rec[0], par)
    meas_parameter = getattr(participant[14].sou[js].rec[jrec], par)
    tremsheet_parameter = getattr(participant[13].sou[js].rec[jrec], par)
    freq_ticks = []
    for f in sou[js].freq:
        freq_ticks.append(str(f))
    fig = plt.figure()
    fig.canvas.set_window_title(par + " vs. freq")
    # title = 'S: ' + str(js) + ', R: ' + str(jrec)
    plt.plot(sou[js].freq, trem_parameter, 's-r', label = softname,
        linewidth = 3)
    plt.plot(participant[14].freq, meas_parameter,
        'o-k', label = 'Measurement', linewidth = 2)
    plt.plot(participant[13].freq, tremsheet_parameter,
        'p-m', label = 'Measurement', linewidth = 2)
    for jp in np.arange(13):
        part_parameter = getattr(participant[jp].sou[js].rec[jrec], par)
        plt.plot(participant[jp].freq,
            part_parameter, '-', linewidth = 1)
    plt.title('Source: ' + str(js+1) + ', Rreceiver: ' + str(jrec+1))
    plt.grid(linestyle = '--')
    plt.legend(loc = 'best')
    plt.xscale('log')
    plt.xticks(sou[js].freq, freq_ticks)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel(par)
    plt.ylim(y_limits)

js = 0
jrec = 1

plot_vs_freq(sou, participant, js, jrec, 'TREM', 'EDT', (0.0, 3.0))
plot_vs_freq(sou, participant, js, jrec, 'TREM', 'T30', (0.0, 3.0))
plot_vs_freq(sou, participant, js, jrec, 'TREM', 'C80', (-4, 8))
plot_vs_freq(sou, participant, js, jrec, 'TREM', 'D50', (0, 100))
plot_vs_freq(sou, participant, js, jrec, 'TREM', 'Ts', (30, 220))
plot_vs_freq(sou, participant, js, jrec, 'TREM', 'G', (0, 15))
plot_vs_freq(sou, participant, js, jrec, 'TREM', 'LF', (0, 40))
plot_vs_freq(sou, participant, js, jrec, 'TREM', 'LFC', (0, 40))

plt.show()

# x_string = ['S1R1','S1R2','S1R3','S2R1','S2R2','S2R3']
# def mount_sr_pairs(participant, jf):
#     parameter = []
#     # t30sr = []
#     # edtsr = []
#     c80sr = []
#     d50sr = []
#     # tssr = []
#     gsr = []
#     # lfsr = []
#     # lfcsr = []
#     for s in np.arange(2):
#         for r in np.arange(3):
#             parameter.append(participant.sou[s].rec[r].T30[jf])
#             # t30sr.append(participant.sou[s].rec[r].T30[jf])
#             # edtsr.append(participant.sou[s].rec[r].EDT[jf])
#             c80sr.append(participant.sou[s].rec[r].C80[jf])
#             d50sr.append(participant.sou[s].rec[r].D50[jf])
#             # tssr.append(participant.sou[s].rec[r].Ts[jf])
#             gsr.append(participant.sou[s].rec[r].G[jf])
#             # lfsr.append(participant.sou[s].rec[r].LF[jf])
#             # lfcsr.append(participant.sou[s].rec[r].LFC[jf])
#     return parameter, c80sr, d50sr, gsr #, t30sr, edtsr, c80sr, d50sr, tssr, gsr, lfsr, lfcsr

# def process_all_participants(participant, jf):
#     T30_part = []
#     # C80_part = []
#     for jp in np.arange(17):
#         T30_part.append(mount_sr_pairs(participant[jp], jf))
#     return T30_part#, C80_part

# def trem_sr_pairs(sou, jf):
#     parameter = []
#     # t30sr = []
#     # edtsr = []
#     c80sr = []
#     d50sr = []
#     # tssr = []
#     gsr = []
#     # lfsr = []
#     # lfcsr = []
#     for s in np.arange(2):
#         for r in np.arange(3):
#             parameter.append(sou[s].rec[r].T30[jf])
#             # t30sr.append(participant.sou[s].rec[r].T30[jf])
#             # edtsr.append(participant.sou[s].rec[r].EDT[jf])
#             c80sr.append(sou[s].rec[r].C80[jf])
#             d50sr.append(sou[s].rec[r].D50[jf])
#             # tssr.append(participant.sou[s].rec[r].Ts[jf])
#             gsr.append(sou[s].rec[r].G[jf])
#             # lfsr.append(participant.sou[s].rec[r].LF[jf])
#             # lfcsr.append(participant.sou[s].rec[r].LFC[jf])
#     return parameter, c80sr, d50sr, gsr #, t30sr, edtsr, c80sr, d50sr, tssr, gsr, lfsr, lfcsr

# jf = 3
# T30_trem, C80_trem, D50_trem, G_trem = trem_sr_pairs(sou, jf)
# T30_meas, C80_meas, D50_meas, G_meas = mount_sr_pairs(participant[17], jf)
# # T30_part = process_all_participants(participant, jf)

# softname = 'TREM'
# fig = plt.figure()
# fig.canvas.set_window_title("T30 vs. S-R pair")
# plt.plot(x_string, T30_meas, 'o-k',
#     label = 'Measurement', linewidth = 2)
# plt.plot(x_string, T30_trem, 's-r',
#     label = softname, linewidth = 2)
# # for jp in np.arange(17):
# #     plt.plot(x_string, T30_part[jp], '-', linewidth = 1)
#     # label = participant[jp].name)
# plt.grid(linestyle = '--')
# plt.legend(loc = 'best')
# plt.title('curtains open.')
# plt.xlabel('Position (S-R pair)')
# plt.ylabel('T30 [s]')
# plt.ylim((0.4, 1.4))
# # plt.show()

# fig = plt.figure()
# fig.canvas.set_window_title("C80 vs. S-R pair")
# plt.plot(x_string, C80_meas, 'o-k',
#     label = 'Measurement', linewidth = 2)
# plt.plot(x_string, C80_trem, 's-r',
#     label = softname, linewidth = 2)
# # for jp in np.arange(17):
# #     plt.plot(x_string, C80_part[jp], '-', linewidth = 1)
#     # label = participant[jp].name)
# plt.grid(linestyle = '--')
# plt.legend(loc = 'best')
# plt.title('curtains open.')
# plt.xlabel('Position (S-R pair)')
# plt.ylabel('C80 [dB]')
# plt.ylim((0, 12))
# # plt.show()

# fig = plt.figure()
# fig.canvas.set_window_title("D50 vs. S-R pair")
# plt.plot(x_string, D50_meas, 'o-k',
#     label = 'Measurement', linewidth = 2)
# plt.plot(x_string, D50_trem, 's-r',
#     label = softname, linewidth = 2)
# # for jp in np.arange(17):
# #     plt.plot(x_string, C80_part[jp], '-', linewidth = 1)
#     # label = participant[jp].name)
# plt.grid(linestyle = '--')
# plt.legend(loc = 'best')
# plt.title('curtains open.')
# plt.xlabel('Position (S-R pair)')
# plt.ylabel('D50 [%]')
# plt.ylim((40, 80))
# # plt.show()

# fig = plt.figure()
# fig.canvas.set_window_title("G vs. S-R pair")
# plt.plot(x_string, G_meas, 'o-k',
#     label = 'Measurement', linewidth = 2)
# plt.plot(x_string, G_trem, 's-r',
#     label = softname, linewidth = 2)
# # for jp in np.arange(17):
# #     plt.plot(x_string, C80_part[jp], '-', linewidth = 1)
#     # label = participant[jp].name)
# plt.grid(linestyle = '--')
# plt.legend(loc = 'best')
# plt.title('curtains open.')
# plt.xlabel('Position (S-R pair)')
# plt.ylabel('G [dB]')
# plt.ylim((16, 24))
# plt.show()


# jp = 17
# js = 1
# jrec = 2
# print("freq: {}".format(participant[jp].name))
# print("freq: {}".format(participant[jp].freq))
# print("T30: {}".format(participant[jp].sou[js].rec[jrec].T30))

# stats.plot_t20_f(plotsr = True)
# plt.show()