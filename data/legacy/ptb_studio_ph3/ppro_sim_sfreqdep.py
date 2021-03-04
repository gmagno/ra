import pickle
import numpy as np
import matplotlib.pyplot as plt
import ra_cpp
from controlsair import load_sim
from rrobin_plots import plot_main_error

#%% classes
def plot_main_error2(sou, sou_scte , participant, softname, par):
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
    fig, ax = plt.subplots()
    # print(par)
    for jpart, p in enumerate(par):
        # print(p)
        error_vector = [] # error vector for posterior plot
        # error_vector_scte = [] # error vector for posterior plot
        part_vector = [] # name of participant for posterior plot
        meas_parameter = [] # a matrix with all source-receiver-frequency bands of measurement (reference)
        trem_parameter = [] # a matrix with all source-receiver-frequency bands of our simulation
        trem_parameter_scte = [] # a matrix with all source-receiver-frequency bands of our simulation
        for js in np.arange(2):
            for jrec in np.arange(3):
                meas_parameter.append(getattr(participant[17].sou[js].rec[jrec], p))
                trem_parameter.append(getattr(sou[js].rec[jrec], p))
                trem_parameter_scte.append(getattr(sou_scte[js].rec[jrec], p))
        
        # The error of our simulation
        if p != 'T30' and p != 'EDT':
            error_trem = np.mean(np.abs(np.array(trem_parameter) - np.array(meas_parameter))) / jnd[p]
            error_trem_scte = np.mean(np.abs(np.array(trem_parameter_scte) - np.array(meas_parameter))) / jnd[p]
        else:
            error_dec = np.zeros(2*3)
            error_dec_scte = np.zeros(2*3)
            for js in np.arange(2*3):
                jnd_decay = np.array(meas_parameter[js] * jnd[p])
                # print(jnd_decay)
                error_dec[js] = np.mean(
                    np.divide(np.abs(np.array(trem_parameter[js]) - np.array(meas_parameter[js])), jnd_decay))
                error_dec_scte[js] = np.mean(
                    np.divide(np.abs(np.array(trem_parameter_scte[js]) - np.array(meas_parameter[js])), jnd_decay))
            error_trem = np.mean(error_dec)
            error_trem_scte = np.mean(error_dec_scte)
        error_vector.append(error_trem_scte)
        error_vector.append(error_trem)

        # Let us find the error of the other participants

        # print(error_vector)
        ind = np.arange(len(error_vector))  # the x locations for the groups
        barwidth = 0.4
        dx = 0.21
        if jpart == 0:
            ax.bar(jpart - dx, error_trem_scte, color = 'tab:blue',
                width = barwidth, label = r'$s = $cte')
            ax.bar(jpart + dx, error_trem, color = 'tab:orange',
                width = barwidth, label = r'$s(f)$')
        else:
            ax.bar(jpart - dx, error_trem_scte, color = 'tab:blue',
                width = barwidth)
            ax.bar(jpart + dx, error_trem, color = 'tab:orange',
                width = barwidth)
        # if len(par) == 2:
        #     if jpart == 0:
        #         ax.bar(ind - width/2, error_vector, width = width, label = p)
        #     else:
        #         ax.bar(ind + width/2, error_vector, width = width, label = p)
        # else:
        #     if jpart == 0:
        #         ax.bar(ind - width, error_vector, width = width, label = p)
        #     elif jpart ==1:
        #         ax.bar(ind, error_vector, width = width, label = p)
        #     else:
        #         ax.bar(ind + width, error_vector, width = width, label = p)
    ax.set_xticks(np.arange(8))
    # part_vector.append(r'$s = $cte')
    # part_vector.append(r'$s(f)$')
    ax.set_xticklabels([r'$T_{30}$', 'EDT', r'$C_{80}$' , r'$D_{50}$', r'$T_s$', r'$G$', 'LF','LFC'])
    # plt.xlabel('TREM data')
    plt.ylabel('rel. mean error')
    plt.legend(loc = 'best')
    plt.tight_layout()
    # plt.bar(part_vector, error_vector, width = 0.65)
    plt.title('Curtains closed')
    plt.grid(linestyle = '--')
    plt.ylim((0, 4.2))
    plt.tight_layout()

class Sou(object):
    def __init__(self, rec):
        self.rec = rec

class Rec():
    def __init__(self, EDT, T20, T30, C80, D50, Ts, G, LF, LFC):
        # Calculate acoustical parameters
        self.EDT = EDT
        self.T20 = T20
        self.T30 = T30
        self.C80 = C80
        self.D50 = D50
        self.Ts = Ts
        self.G = G
        self.LF = LF
        self.LFC = LFC
#%% Freq
freq = [125,250,500,1000,2000,4000]
#%% Load
path = '/home/eric/dev/ra/data/legacy/ptb_studio_ph3/'
results = []
for jf, f in enumerate(freq):
    pkl_fname_res = 'ptb_ph3_o_'+str(int(f))+'Hz'        # simulation results name
    print('Reading file: {}'.format(pkl_fname_res))
    controls, air, rays_i, geometry,\
        stats_theory, sources, receivers,\
        s_reflecto_par, stats_analysis = load_sim(path=path, fname=pkl_fname_res)
    results.append(s_reflecto_par)
    # print(s_reflecto_par[1].rec[2].T30)
#%% Process all S-R pairs for all freq bands
sou = []
for js in np.arange(2):
    rec = []
    for jr in np.arange(3):
        EDT = []
        T20 = []
        T30 = []
        C80 = []
        D50 = []
        Ts = []
        G = []
        LF = []
        LFC = []
        for jf, f in enumerate(freq):
            res_jf = results[jf]
            EDT.append(res_jf[js].rec[jr].EDT[jf])
            T20.append(res_jf[js].rec[jr].T20[jf])
            T30.append(res_jf[js].rec[jr].T30[jf])
            C80.append(res_jf[js].rec[jr].C80[jf])
            D50.append(res_jf[js].rec[jr].D50[jf])
            Ts.append(res_jf[js].rec[jr].Ts[jf])
            G.append(res_jf[js].rec[jr].G[jf])
            LF.append(res_jf[js].rec[jr].LF[jf])
            LFC.append(res_jf[js].rec[jr].LFC[jf])
        rec.append(Rec(EDT, T20, T30, C80, D50, Ts, G, LF, LFC))
    sou.append(Sou(rec))

#%% RR III load data
# Load round robin data
print('load round robin data')
pkl_fname = 'data/legacy/ptb_studio_ph3/rrobin3_par_open.pkl'
# pkl_fname = 'data/legacy/ptb_studio_ph3/rrobin3_par_closed.pkl'
with open(pkl_fname, 'rb') as input:
    participant = pickle.load(input)

#%% 
plot_main_error(sou, participant, '(T)', ('T30','EDT', 'G'))
# plt.savefig(path + 'figs/' + 'error_t30_edt_g' + '.png')
# plt.savefig(path + 'figs/' + 'error_t30_edt_g' + '.pdf')
# plt.savefig(path + 'figs/' + 'error_t30_edt_g' + '.eps')
plot_main_error(sou, participant, '(T)', ('C80','D50', 'Ts'))
# plt.savefig(path + 'figs/' + 'error_c80_d50_ts' + '.png')
# plt.savefig(path + 'figs/' + 'error_c80_d50_ts' + '.pdf')
# plt.savefig(path + 'figs/' + 'error_c80_d50_ts' + '.eps')
plot_main_error(sou, participant, '(T)', ('LF', 'LFC'))
# plt.savefig(path + 'figs/' + 'error_lf_lfc' + '.png')
# plt.savefig(path + 'figs/' + 'error_lf_lfc' + '.pdf')
# plt.savefig(path + 'figs/' + 'error_c80_d50_ts' + '.eps')

plot_main_error2(sou, results[3] , participant, '(T)', ('T30','EDT', 'G','C80','D50', 'Ts', 'LF','LFC'))
# plot_main_error2(sou, results[3] , participant, '(T)', ('C80','D50', 'Ts'))# 
# plot_main_error2(sou, results[3] , participant, '(T)', ('LF','LFC'))# 


plt.show()
#%% tests
# res_jf125 = results[0]
# res_jf250 = results[1]
# res_jf500 = results[2]
# res_jf1000 = results[3]
# res_jf2000 = results[4]
# res_jf4000 = results[5]

# print(res_jf125[0].rec[0].T30)
# print(res_jf250[0].rec[0].T30)
# print(res_jf500[0].rec[0].T30)
# print(res_jf1000[0].rec[0].T30)
# print(res_jf2000[0].rec[0].T30)
# print(res_jf4000[0].rec[0].T30)

# print(sou[0].rec[0].T30)

