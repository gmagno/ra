import pickle
# import pandas as pd
import xlrd
import numpy as np
import matplotlib.pyplot as plt
# from ra.results import SRStats
from ppro_rrobin_classes import ParRoundRobin, SouRoundRobin, RecRoundRobin



def read_participant(file_name, jpar, open = True):
    sou = []
    if open:
        jsr = 1 # 1 for curtain open, 9 for curtaion close
    else:
        jsr = 9
    for s in np.arange(2):
        rec = []
        for r in np.arange(3):
            # print('Reading source {} and receiver {}.'.format(s, r))
            rec.append(RecRoundRobin(file_name, jpar, jsr))
            jsr += 1
        sou.append(SouRoundRobin(rec))
    return sou

file_name = 'data/legacy/ptb_studio_ph3/ptb_ph3_edited.xls'
wb = xlrd.open_workbook(file_name)
sheet_names = wb.sheet_names()
participant = []
for jpar in np.arange(2,20):
    print('Reading participant {}.'.format(jpar))
    sou = read_participant(file_name, jpar, open = False)
    # participant.append(sou)
    participant.append(ParRoundRobin(sou, sheet_names[jpar]))


# Save to pickle
pkl_fname = 'data/legacy/ptb_studio_ph3/rrobin3_par_closed.pkl'
with open(pkl_fname, 'wb') as output:
    pickle.dump(participant, output, pickle.HIGHEST_PROTOCOL)
# print(participant[0])

jp = 17
js = 1
jrec = 2

print("freq: {}".format(participant[jp].name))
print("freq: {}".format(participant[jp].freq))
print("T30: {}".format(participant[jp].sou[js].rec[jrec].T30))

# print("T30: {}".format(participant[jp][js].rec[jrec].T30))
# print("EDT: {}".format(participant[jp][js].rec[jrec].EDT))
# print("D50: {}".format(participant[jp][js].rec[jrec].D50))
# print("C80 {}".format(participant[jp][js].rec[jrec].C80))
# print("Ts {}".format(participant[jp][js].rec[jrec].Ts))
# print("G: {}".format(participant[jp][js].rec[jrec].G))
# print("LF: {}".format(participant[jp][js].rec[jrec].LF))
# print("LFC: {}".format(participant[jp][js].rec[jrec].LFC))

# # For row 0 and column 0
# print(sheet.cell_value(4, 1))
# df = pd.read_excel (r'data/legacy/ptb_studio_ph2/ptb_ph3_edited.xls', sheet_name=2)
# print(df)
# print(type(df))
# print(df(4,1))

