import pickle
import numpy as np
import matplotlib.pyplot as plt
from ra.results import SRStats
from data.legacy.ptb_studio_ph3.ppro_rrobin_classes import ParRoundRobin, SouRoundRobin, RecRoundRobin

SMALL_SIZE = 10
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

# Load round robin data
print('load round robin data')
pkl_fname = 'data/legacy/ptb_studio_ph3/rrobin3_par_open.pkl'
# pkl_fname = 'data/legacy/ptb_studio_ph3/rrobin3_par_closed.pkl'
with open(pkl_fname, 'rb') as input:
    participant = pickle.load(input)

# Load TREM data
print('load trem data')
path = 'data/legacy/ptb_studio_ph3/'    # room folder
pkl_fname_res = 'ptb_studio_ph3_open'        # simulation results name
with open(path+pkl_fname_res+'.pkl', 'rb') as input:
    res_stat = pickle.load(input)
    sou = pickle.load(input)
    stats = pickle.load(input)

def plot_vs_freq(sou, participant, js, jrec, softname, par, y_limits):
    '''
    Function to plot parameter vs. frequency for a specified source-receiver pair.
    TREM vs measured data vs all participant.
    '''
    par_title = {'T30': r'$T_{30}$ [s]', 'EDT': 'EDT [s]', 'C80': r'$C_{80}$ [dB]', 'D50': r'$D_{50}$ [%]',
        'Ts': r'$T_{s}$ [ms]', 'G': r'$G$ [dB]', 'LF': 'LF [%]', 'LFC': 'LFC [%]'}
    trem_parameter = getattr(sou[js].rec[jrec], par)
    meas_parameter = getattr(participant[17].sou[js].rec[jrec], par)
    freq_ticks = []
    for f in sou[js].freq:
        freq_ticks.append(str(f))
    fig = plt.figure()
    fig.canvas.set_window_title(par + " vs. freq")
    # title = 'S: ' + str(js) + ', R: ' + str(jrec)
    # plt.plot(sou[js].freq, res_stat.t60_e, 's-m', label = 'Eyring',
    #     linewidth = 3)
    plt.plot(sou[js].freq, trem_parameter, 's-r', label = softname,
        linewidth = 3)
    plt.plot(participant[17].freq, meas_parameter,
        'o-k', label = 'Measurement', linewidth = 2)
    for jp in np.arange(17):
        part_parameter = getattr(participant[jp].sou[js].rec[jrec], par)
        plt.plot(participant[jp].freq,
            part_parameter, '-', color = 'grey', linewidth = 1)
    plt.title('Source: ' + str(js+1) + ', Rreceiver: ' + str(jrec+1))
    plt.grid(linestyle = '--')
    plt.legend(loc = 'best')
    plt.xscale('log')
    plt.xticks(sou[js].freq, freq_ticks)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel(par_title[par])
    plt.ylim(y_limits)

def plot_vs_srpairs(sou, participant, jf, softname, par, y_limits):
    '''
    Function to plot parameter vs. sr-pairs for a specified frequency band.
    TREM vs measured data vs all participant.
    '''
    par_title = {'T30': r'$T_{30}$ [s]', 'EDT': 'EDT [s]', 'C80': r'$C_{80}$ [dB]', 'D50': r'$D_{50}$ [%]',
        'Ts': r'$T_{s}$ [ms]', 'G': r'$G$ [dB]', 'LF': 'LF [%]', 'LFC': 'LFC [%]'}
    trem_parameter = []
    meas_parameter = []
    for js in np.arange(2):
        for jrec in np.arange(3):
            trem_parameter_vec = getattr(sou[js].rec[jrec], par)
            trem_parameter.append(trem_parameter_vec[jf])
            meas_parameter_vec = getattr(participant[17].sou[js].rec[jrec], par)
            meas_parameter.append(meas_parameter_vec[jf])
    # read all participants
    part_matrix = []
    for jp in np.arange(17):
        part_parameter = []
        for js in np.arange(2):
            for jrec in np.arange(3):
                participant_parameter_vec = getattr(participant[jp].sou[js].rec[jrec], par)
                part_parameter.append(participant_parameter_vec[jf])
        part_matrix.append(part_parameter)

    x_string = ['S1R1','S1R2','S1R3','S2R1','S2R2','S2R3']

    fig = plt.figure()
    fig.canvas.set_window_title(par + " vs. SR pair")
    # title = 'S: ' + str(js) + ', R: ' + str(jrec)
    # plt.plot(sou[js].freq, res_stat.t60_e, 's-m', label = 'Eyring',
    #     linewidth = 3)
    plt.plot(x_string, trem_parameter, 's-r', label = softname,
        linewidth = 3)
    plt.plot(x_string, meas_parameter, 'o-k', label = 'Measurement',
        linewidth = 2)
    for jp in np.arange(17):
        plt.plot(x_string, part_matrix[jp], '-', color = 'grey', linewidth = 1)
    plt.title('Frequency band: ' + str(sou[0].freq[jf]) + ' Hz')
    plt.grid(linestyle = '--')
    plt.legend(loc = 'best')
    plt.xticks(np.arange(6), x_string)
    plt.xlabel('Position')
    plt.ylabel(par_title[par])
    plt.ylim(y_limits)

def plot_all_vsfreq(sou, participant, softname, path):
    '''
    Function to plot par vs freq for all SR pairs and save all the results.
    '''
    par_vec = ['T30', 'EDT', 'C80', 'D50', 'Ts', 'G', 'LF', 'LFC']
    range_vec = [(0.0, 1.4), (0.0, 1.4), (0, 12), (0, 100), (30, 90), (0, 24), (0, 40), (0, 50)]
    for jpar, par in enumerate(par_vec):
        for js in np.arange(2):
            for jrec in np.arange(3):
                plot_vs_freq(sou, participant, js, jrec, 'Trem', par, range_vec[jpar])
                filename = par + '_S' + str(js+1)+ '_R' + str(jrec+1)
                plt.savefig(path + 'figs/' + filename + '.png')
                plt.savefig(path + 'figs/' + filename + '.pdf')

def plot_all_srpairs(sou, participant, softname, path):
    '''
    Function to plot par vs sr pair for all frequency bands and save all the results.
    '''
    par_vec = ['T30', 'EDT', 'C80', 'D50', 'Ts', 'G', 'LF', 'LFC']
    range_vec = [(0.0, 1.4), (0.0, 1.4), (0, 12), (0, 100), (30, 90), (0, 24), (0, 40), (0, 50)]
    for jpar, par in enumerate(par_vec):
        for jf, f in enumerate(sou[0].freq):
            plot_vs_srpairs(sou, participant, jf, 'Trem', par, range_vec[jpar])
            filename = par + 'freq' + str(int(f))+ '_Hz'
            plt.savefig(path + 'figs/' + filename + '.png')
            plt.savefig(path + 'figs/' + filename + '.pdf')


def plot_main_error(sou, participant, softname, par):
    '''
    Function to plot RMS error / jnd.
    '''
    jnd = {'T30': 0.05, 'EDT': 0.05, 'C80': 1, 'D50': 5, 'Ts': 10, 'G': 1.0, 'LF': 5, 'LFC': 5}
    if len(par) == 2:
        width = 0.4  # the width of the bars
    else:
        width = 0.3
    # fig = plt.figure()
    # fig.canvas.set_window_title('Total ratio of RMS error by jnd of: ' + p)
    fig, ax = plt.subplots(figsize=(9, 4))
    for jpart, p in enumerate(par):
        error_vector = [] # error vector for posterior plot
        part_vector = [] # name of participant for posterior plot
        meas_parameter = [] # a matrix with all source-receiver-frequency bands of measurement (reference)
        trem_parameter = [] # a matrix with all source-receiver-frequency bands of our simulation
        for js in np.arange(2):
            for jrec in np.arange(3):
                meas_parameter.append(getattr(participant[17].sou[js].rec[jrec], p))
                trem_parameter.append(getattr(sou[js].rec[jrec], p))
        # The error of our simulation
        if p != 'T30' and p != 'EDT':
            error_trem = np.mean(np.abs(np.array(trem_parameter) - np.array(meas_parameter))) / jnd[p]
        else:
            error_dec = np.zeros(2*3)
            for js in np.arange(2*3):
                jnd_decay = np.array(meas_parameter[js] * jnd[p])
                # print(jnd_decay)
                error_dec[js] = np.mean(
                    np.divide(np.abs(np.array(trem_parameter[js]) - np.array(meas_parameter[js])), jnd_decay))
            error_trem = np.mean(error_dec)
        # Let us find the error of the other participants

        for jp in np.arange(17):
            part_vector.append(str(jp+1))
            part_parameter = []
            for js in np.arange(2):
                for jrec in np.arange(3):
                    part_parameter.append(getattr(participant[jp].sou[js].rec[jrec], p))
            if p != 'T30' or p != 'EDT':
                error_part = np.mean(np.abs(np.array(part_parameter) - np.array(meas_parameter))) / jnd[p]
            else:
                error_dec = np.zeros(2*3)
                for js in np.arange(2*3):
                    jnd_decay = np.array(meas_parameter[js] * jnd[p])
                    error_dec[js] = np.mean(
                    np.divide(np.abs(np.array(part_parameter[js]) - np.array(meas_parameter[js])), jnd_decay))
                error_part = np.mean(error_dec)
            error_vector.append(error_part)
        error_vector.append(error_trem)
        part_vector.append(softname)
        # print(error_vector)
        ind = np.arange(len(error_vector))  # the x locations for the groups
        if len(par) == 2:
            if jpart == 0:
                ax.bar(ind - width/2, error_vector, width = width, label = p)
            else:
                ax.bar(ind + width/2, error_vector, width = width, label = p)
        else:
            if jpart == 0:
                ax.bar(ind - width, error_vector, width = width, label = p)
            elif jpart ==1:
                ax.bar(ind, error_vector, width = width, label = p)
            else:
                ax.bar(ind + width, error_vector, width = width, label = p)
    ax.set_xticks(ind)
    ax.set_xticklabels(part_vector)
    plt.xlabel('participant')
    plt.ylabel('rel. mean error')
    plt.legend(loc = 'best')
    plt.tight_layout()
    # plt.bar(part_vector, error_vector, width = 0.65)
    # plt.title('Total ratio of RMS error by jnd of: ' + p)
    plt.grid(linestyle = '--')


plot_all_vsfreq(sou, participant, 'Trem', path)
plot_all_srpairs(sou, participant, 'Trem', path)
# plot_main_error(sou, participant, '(T)', ('T30','EDT', 'G'))
# plt.savefig(path + 'figs/' + 'error_t30_edt_g' + '.png')
# plt.savefig(path + 'figs/' + 'error_t30_edt_g' + '.pdf')
# plt.savefig(path + 'figs/' + 'error_t30_edt_g' + '.eps')
# plot_main_error(sou, participant, '(T)', ('C80','D50', 'Ts'))
# plt.savefig(path + 'figs/' + 'error_c80_d50_ts' + '.png')
# plt.savefig(path + 'figs/' + 'error_c80_d50_ts' + '.pdf')
# plt.savefig(path + 'figs/' + 'error_c80_d50_ts' + '.eps')
# plot_main_error(sou, participant, '(T)', ('LF', 'LFC'))
# plt.savefig(path + 'figs/' + 'error_lf_lfc' + '.png')
# plt.savefig(path + 'figs/' + 'error_lf_lfc' + '.pdf')
# plt.savefig(path + 'figs/' + 'error_c80_d50_ts' + '.eps')
# plt.show()
# js = 0
# jrec = 0
# jf = 3
# plot_vs_freq(sou, participant, js, jrec, 'TREM', 'T30', (0.4, 1.4))
# plot_vs_srpairs(sou, participant, jf, 'TREM', 'D50', (0, 100))
# plt.show()


# def plot_main_error(sou, participant, softname, par, y_limits):
#     '''
#     Function to plot RMS error / jnd.
#     '''
#     jnd = {'T30': 0.1, 'EDT': 0.1, 'C80': 1, 'D50': 10, 'Ts': 10, 'G': 1.0, 'LF': 1.0, 'LFC': 1.0}
#     error_vector = [] # error vector for posterior plot
#     part_vector = [] # name of participant for posterior plot
#     meas_parameter = [] # a matrix with all source-receiver-frequency bands of measurement (reference)
#     trem_parameter = [] # a matrix with all source-receiver-frequency bands of our simulation
#     for js in np.arange(2):
#         for jrec in np.arange(3):
#             meas_parameter.append(getattr(participant[17].sou[js].rec[jrec], par))
#             trem_parameter.append(getattr(sou[js].rec[jrec], par))
#     # The error of our simulation
#     error_trem = np.mean(np.abs(np.array(trem_parameter) - np.array(meas_parameter))) / jnd[par]
#     # Let us find the error of the other participants

#     for jp in np.arange(17):
#         part_vector.append(str(jp+1))
#         part_parameter = []
#         for js in np.arange(2):
#             for jrec in np.arange(3):
#                 part_parameter.append(getattr(participant[jp].sou[js].rec[jrec], par))
#         error_part = np.mean(np.abs(np.array(part_parameter) - np.array(meas_parameter))) / jnd[par]
#         error_vector.append(error_part)
#     error_vector.append(error_trem)
#     part_vector.append(softname)
#     # print(error_vector)
#     ind = np.arange(len(error_vector))  # the x locations for the groups
#     width = 0.35  # the width of the bars
#     fig = plt.figure()
#     fig.canvas.set_window_title('Total ratio of RMS error by jnd of: ' + par)
#     fig, ax = plt.subplots()
#     ax.bar(ind - width/2, error_vector, width = width)
#     ax.bar(ind + width/2, np.array(error_vector)-0.3, width = width)
#     ax.set_xticks(ind)
#     ax.set_xticklabels(part_vector)
#     # plt.bar(part_vector, error_vector, width = 0.65)
#     plt.title('Total ratio of RMS error by jnd of: ' + par)
#     plt.grid(linestyle = '--')



# x_string = ['S1R1','S1R2','S1R3','S2R1','S2R2','S2R3']
# def mount_sr_pairs(participant, jf):
#     # parameter = []
#     t30sr = []
#     edtsr = []
#     c80sr = []
#     d50sr = []
#     tssr = []
#     gsr = []
#     lfsr = []
#     lfcsr = []
#     for s in np.arange(2):
#         for r in np.arange(3):
#             # parameter.append(participant.sou[s].rec[r].T30[jf])
#             t30sr.append(participant.sou[s].rec[r].T30[jf])
#             edtsr.append(participant.sou[s].rec[r].EDT[jf])
#             c80sr.append(participant.sou[s].rec[r].C80[jf])
#             d50sr.append(participant.sou[s].rec[r].D50[jf])
#             tssr.append(participant.sou[s].rec[r].Ts[jf])
#             gsr.append(participant.sou[s].rec[r].G[jf])
#             lfsr.append(participant.sou[s].rec[r].LF[jf])
#             lfcsr.append(participant.sou[s].rec[r].LFC[jf])
#     return t30sr, edtsr, c80sr, d50sr, tssr, gsr, lfsr, lfcsr

# def trem_sr_pairs(sou, jf):
#     # parameter = []
#     t30sr = []
#     edtsr = []
#     c80sr = []
#     d50sr = []
#     tssr = []
#     gsr = []
#     lfsr = []
#     lfcsr = []
#     for s in np.arange(2):
#         for r in np.arange(3):
#             # parameter.append(sou[s].rec[r].T30[jf])
#             t30sr.append(sou[s].rec[r].T30[jf])
#             edtsr.append(sou[s].rec[r].EDT[jf])
#             c80sr.append(sou[s].rec[r].C80[jf])
#             d50sr.append(sou[s].rec[r].D50[jf])
#             tssr.append(sou[s].rec[r].Ts[jf])
#             gsr.append(sou[s].rec[r].G[jf])
#             lfsr.append(sou[s].rec[r].LF[jf])
#             lfcsr.append(sou[s].rec[r].LFC[jf])
#     return t30sr, edtsr, c80sr, d50sr, tssr, gsr, lfsr, lfcsr

# def process_all_participants(participant, jf):
#     T30_part = []
#     # C80_part = []
#     for jp in np.arange(17):
#         T30_part.append(mount_sr_pairs(participant[jp], jf))
#     return T30_part#, C80_part

# jf = 3
# T30_trem, EDT_trem, C80_trem, D50_trem, Ts_trem, G_trem, LF_trem, LFC_trem = trem_sr_pairs(sou, jf)
# # print(T30_trem)
# T30_meas, EDT_meas, C80_meas, D50_meas, Ts_meas, G_meas, LF_meas, LFC_meas = mount_sr_pairs(participant[17], jf)
# # print(T30_meas)



# T30_part = process_all_participants(participant, jf)
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