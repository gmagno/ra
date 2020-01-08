import pickle
import xlrd
import numpy as np
import matplotlib.pyplot as plt

class DatabaseInperpolator():
    def __init__(self, freq, alpha):
        self.freq = freq
        self.alpha = alpha
        self.freq_ticks = []
        for f in self.freq:
            self.freq_ticks.append(str(f))

    def get_valid(self,):
        alpha_id = np.where(self.alpha != 0)[0]
        self.alpha_valid = self.alpha[alpha_id]
        self.freq_valid = self.freq[alpha_id]

    def make_interpolation(self, degree = 5):
        '''
        Makes interpolation: For lower frequencies a polynomial fit of the first 3 bads
        with a specified degree (5 default). For last band (usually missing) it is a
        linear fit of the last 2 freq bands
        '''
        # all bands
        coefs = np.polyfit(self.freq_valid, self.alpha_valid, degree)
        p = np.poly1d(coefs)
        self.freq_final = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
        self.alpha_final = p(self.freq_final)
        # higher band
        coefs = np.polyfit(self.freq_valid[self.freq_valid.size-2:],
            self.alpha_valid[self.freq_valid.size-2:], 1)
        p = np.poly1d(coefs)
        self.alpha_final[-1] = p(self.freq_final[-1])
        # lower bands
        coefs = np.polyfit(self.freq_valid[0:2],
            self.alpha_valid[0:2], degree)
        p = np.poly1d(coefs)
        self.alpha_final[0:2] = p(self.freq_final[0:2])

    def restore_original_valids(self,):
        for jf, f in enumerate(self.freq):
            freq_id = np.where(self.freq_valid == f)[0]
            if freq_id.size != 0:
                jfv = np.where(self.freq_final == f)[0]
                self.alpha_final[jfv] = self.alpha[jf]

    def change_invalids(self,):
        '''
        Eliminate negatives, zeros and bigger than 1 values
        '''
        # lower or equal than zero
        alpha_id = np.where(self.alpha_final <= 0)[0]
        self.alpha_final[alpha_id] = 0.01
        # bigger than 1.00
        alpha_id = np.where(self.alpha_final > 1.0)[0]
        self.alpha_final[alpha_id] = 0.99

    def plot_abs(self,):
        fig = plt.figure()
        fig.canvas.set_window_title("alpha")
        plt.plot(self.freq_valid, self.alpha_valid, 'o-k',
            label = 'original', linewidth = 4)
        plt.plot(self.freq_final, self.alpha_final, 'o-b',
            label = 'interpolated', linewidth = 1)
        plt.grid(linestyle = '--')
        plt.legend(loc = 'best')
        plt.xscale('log')
        plt.title('alpha and alpha interpolated.')
        plt.xticks(self.freq, self.freq_ticks)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('\alpha [s]')
        plt.ylim((-0.2, 1.2))
        plt.show()


file_name = '/home/eric/dev/ra/data/material/abstab_wf.xls'
wb = xlrd.open_workbook(file_name)
sheet_names = wb.sheet_names()
sheet = wb.sheet_by_index(1)
freq_original = np.float32([63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630,
	800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000])

Nmat = 2571
material_list = []
for jmat in np.arange(Nmat):
    print('Reading material {} of Nmat {} materials'.format(jmat+1, Nmat))
    mat_id = int(sheet.cell_value(jmat+20, 0))
    mat_name = sheet.cell_value(jmat+20, 1)
    alpha = np.array(sheet.row_values(
        jmat+20, start_colx=14, end_colx=36))
    alpha[alpha==''] = '0'
    alpha = alpha.astype(np.float32)
    # print(mat_name)
    interpolator = DatabaseInperpolator(freq_original, alpha)
    interpolator.get_valid()
    interpolator.make_interpolation(degree = 1)
    interpolator.restore_original_valids()
    interpolator.change_invalids()
    # interpolator.plot_abs()
    material_list.append(
        {'id': mat_id,
        'Description': mat_name,
        'alpha': interpolator.alpha_final})

import csv
with open('absorption_database.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'Description', 'alpha']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for material in material_list:
        writer.writerow(material)

# with open('absorption_database.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print(row['id'], row['Description'], row['alpha'])
