import pickle
import pandas as pd
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from ra.results import SRStats

class SouRoundRobin(object):
    def __init__(self, recdata):
        self.freq = np.array((125, 250, 500, 1000, 2000, 4000), dtype = np.float32)
        self.rec = recdata

class RecRoundRobin():
    def __init__(self, file_name, participant, jsr):
        # To open Workbook
        wb = xlrd.open_workbook(file_name)
        sheet = wb.sheet_by_index(participant)
        T30_i = 3 # valid for the round robin 3
        step = 12 # valid for the round robin 3
        freq = np.array((125, 250, 500, 1000, 2000, 4000), dtype = np.float32)
        self.T30 = np.zeros((len(freq)), dtype = np.float32)
        self.EDT = np.zeros((len(freq)), dtype = np.float32)
        self.D50 = np.zeros((len(freq)), dtype = np.float32)
        self.C80 = np.zeros((len(freq)), dtype = np.float32)
        self.Ts = np.zeros((len(freq)), dtype = np.float32)
        self.G = np.zeros((len(freq)), dtype = np.float32)
        self.LF = np.zeros((len(freq)), dtype = np.float32)
        self.LFC = np.zeros((len(freq)), dtype = np.float32)
        idf = T30_i
        for jf, f in enumerate(freq):
            self.T30[jf] = sheet.cell_value(idf, jsr)
            self.EDT[jf] = sheet.cell_value(idf+1, jsr)
            self.D50[jf] = sheet.cell_value(idf+2, jsr)
            self.C80[jf] = sheet.cell_value(idf+3, jsr)
            self.Ts[jf] = sheet.cell_value(idf+4, jsr)
            self.G[jf] = sheet.cell_value(idf+5, jsr)
            self.LF[jf] = sheet.cell_value(idf+6, jsr)
            self.LFC[jf] = sheet.cell_value(idf+7, jsr)
            idf += step

def read_participant(file_name, jpar, open = True):
    sou = []
    if open:
        jsr = 1 # 1 for curtain open, 9 for curtaion close
    else:
        jsr = 9
    for s in np.arange(2):
        rec = []
        for r in np.arange(3):
            rec.append(RecRoundRobin(file_name, jpar, jsr))
            jsr += 1
        sou.append(SouRoundRobin(rec))
    return sou

file_name = 'data/legacy/ptb_studio_ph2/ptb_ph3_edited.xls'
participant = []
for jpar in np.arange(2,19):
    sou = read_participant(file_name, jpar)
    participant.append(sou)

print(participant[0])

jp = 0
js = 1
jrec = 2

print("T30: {}".format(participant[jp][js].rec[jrec].T30))
print("EDT: {}".format(participant[jp][js].rec[jrec].EDT))
print("D50: {}".format(participant[jp][js].rec[jrec].D50))
print("C80 {}".format(participant[jp][js].rec[jrec].C80))
print("Ts {}".format(participant[jp][js].rec[jrec].Ts))
print("G: {}".format(participant[jp][js].rec[jrec].G))
print("LF: {}".format(participant[jp][js].rec[jrec].LF))
print("LFC: {}".format(participant[jp][js].rec[jrec].LFC))

# # For row 0 and column 0
# print(sheet.cell_value(4, 1))
# df = pd.read_excel (r'data/legacy/ptb_studio_ph2/ptb_ph3_edited.xls', sheet_name=2)
# print(df)
# print(type(df))
# print(df(4,1))

