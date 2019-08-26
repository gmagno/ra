import xlrd
import numpy as np
import matplotlib.pyplot as plt

class ParRoundRobin(object):
    def __init__(self, soudata, name):
        self.freq = np.array((125, 250, 500, 1000, 2000, 4000), dtype = np.float32)
        self.sou = soudata
        self.name = name

class SouRoundRobin(object):
    def __init__(self, recdata):
        # self.freq = np.array((125, 250, 500, 1000, 2000, 4000), dtype = np.float32)
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