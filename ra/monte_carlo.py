import numpy as np
import matplotlib.pyplot as plt
from statistics import StatisticalMat

class MCRoomAcoustics(object):
    '''
    A class to run a Monte Carlo simlulation for room acoustics
    '''
    def __init__(self, controls = [], air = [],
    geometry = [], stats_theory = [], sources = [], Nmc = 20):
        self.controls = controls
        self.air = air
        self.geometry = geometry
        self.stats_theory = stats_theory
        self.sources = sources
        self.Nmc = Nmc

    def create_abs_pop(self, rel_std = 0.2):
        '''
        This method is used to create a population of materials for each room surface
        '''
        self.plane_mc_alpha = []
        for plane in self.geometry.planes:
            abs_mtx = (rel_std*plane.alpha) * np.random.randn(self.Nmc, len(self.controls.freq)) + plane.alpha
            # We should correct for larger values than 1
            abs_mtx[abs_mtx >=1.0] = (1-rel_std) + rel_std * np.random.rand(len(abs_mtx[abs_mtx >=1.0]))
            abs_mtx[abs_mtx <=0.0] = 0.01 + 0.05 * np.random.rand(len(abs_mtx[abs_mtx <=0.0]))
            # ids = np.where(abs_mtx <= 0.0)
            # abs_mtx[ids[0]] = 0.001
            # ids = np.where(abs_mtx >= 1.0)
            # print(ids)
            # abs_mtx[ids[0]] = 1.0
            self.plane_mc_alpha.append(abs_mtx)
            # print(plane.alpha)

    def run_mc(self, statistical = True, ray_tracing = False):
        '''
        Computes the monte carlo analysis
        '''
        # Allocate memory
        if statistical:
            t60_sabine_ind = np.zeros((self.Nmc, len(self.controls.freq)))
        # you need to compute parameters for each MC iteration
        for jmc in np.arange(0, stop = self.Nmc):
            # parse geometry data
            geo_dummy = self.geometry
            geo_dummy = parse_geometry(geo_dummy, self.plane_mc_alpha, jmc)
            # print('mc sample {}, alpha: {}'.format(jmc, geo_dummy.planes[1].alpha))
            statistical_obj = StatisticalMat(geo_dummy, self.controls.freq, self.air.c0, self.air.m)
            t60_sabine_ind[jmc, :] = statistical_obj.t60_sabine()
            # res_stat.t60_eyring()
            # res_stat.t60_kutruff(gamma=0.4)
            # res_stat.t60_araup()
            # res_stat.t60_fitzroy()
            # res_stat.t60_milsette()
            # res_stat.plot_t60()

        # Draw statistical data
        if statistical:
            self.t60_sabine_mean = np.mean(t60_sabine_ind, axis=0)
            self.t60_sabine_std = np.std(t60_sabine_ind, axis=0)

    def plot_absorption(self, desired_plane = 0):
        '''
        Plots absorption and confidence interval for a given plane.
        '''
        ### calculations
        mat_mean = np.mean(self.plane_mc_alpha[desired_plane], axis=0)
        mat_std = np.std(self.plane_mc_alpha[desired_plane], axis=0)
        ###### Figure
        freq_ticks = [str(f) for f in self.controls.freq]
        fig = plt.figure()
        fig.canvas.set_window_title('Absorption coefficient of Monte Carlo distribution for plane {}'.format(desired_plane))
        plt.semilogx(self.controls.freq, self.geometry.planes[desired_plane].alpha, 'o-k',
            linewidth = 3.0, label = 'original value')
        plt.semilogx(self.controls.freq, mat_mean, 'o-r',
            linewidth = 2.0, label = 'mean from MC distribution')
        plt.fill_between(self.controls.freq, mat_mean - mat_std, mat_mean + mat_std,
            alpha = 0.3, color='grey', label = r'$\mu_x \pm \sigma_x$')
        # for jp in np.arange(self.Nmc):
        #     plt.semilogx(self.controls.freq, self.plane_mc_alpha[desired_plane][jp], color = 'blue',
        #         linewidth = 1.0)
        plt.grid(linestyle = '--')
        plt.legend(loc = 'upper left')
        plt.xticks(self.controls.freq, freq_ticks)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel(r'$\alpha$ [-]')
        plt.ylim((-0.20, 1.2))

    def plot_t60_sabine(self, ci = 1.96):
        '''
        Plots Reverberation time given by Sabine's formula out of MC simulation.
        '''
        ###### Figure
        freq_ticks = [str(f) for f in self.controls.freq]
        fig = plt.figure()
        fig.canvas.set_window_title("T60 Sabine's Formula") 
        plt.title("T60 - Sabine's Formula")
        plt.semilogx(self.controls.freq, self.stats_theory.t60_s, 'o-k',
            linewidth = 3.0, label = 'original value')
        plt.semilogx(self.controls.freq, self.t60_sabine_mean, 'o-r',
            linewidth = 2.0, label = 'mean from MC distribution')
        plt.fill_between(self.controls.freq, self.t60_sabine_mean - ci*self.t60_sabine_std,
            self.t60_sabine_mean + ci*self.t60_sabine_std,
            alpha = 0.3, color='grey', label = 'conf. interval')
        # for jp in np.arange(self.Nmc):
        #     plt.semilogx(self.controls.freq, self.plane_mc_alpha[desired_plane][jp], color = 'blue',
        #         linewidth = 1.0)
        plt.grid(linestyle = '--')
        plt.legend(loc = 'lower left')
        plt.xticks(self.controls.freq, freq_ticks)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('T60 (Sabine) [s]')
        # plt.ylim((-0.20, 1.2))

    def plot_histogram(self, desired_plane = 0, rel_hist = False):
        '''
        This method will plot a histogram for each frequency band of the absorption coefficient.
        '''
        alpha_pop = self.plane_mc_alpha[desired_plane]
        fig = plt.figure(figsize=(15.75, 10.5))
        fig.canvas.set_window_title('Histogram for plane {}'.format(desired_plane))
        # loop over frequency bands
        for jf, freq in enumerate(self.controls.freq):
            plt.subplot(2, 4, jf+1)
            plt.title('{} Hz'.format(freq))
            if rel_hist:
                plt.hist(alpha_pop[:,jf], bins = np.linspace(start = 0, stop = 1, num = 20),
                    weights=np.zeros_like(alpha_pop[:,jf]) + 1. / alpha_pop[:,jf].size)
                plt.ylim((0, 1.0))
            else:
                plt.hist(alpha_pop[:,jf], bins = np.linspace(start = 0, stop = 1, num = 20))
            plt.grid(linestyle = '--', which='both')
            plt.xlim((0, 1.0))
            plt.xlabel(r'$\alpha$ [-]')
            plt.ylabel('Num. of ocurrences')
        fig.tight_layout()

def parse_geometry(geometry, plane_mc_alpha, jmc):
    '''
    A function to re-write absorption data from MC samples on the geometry
    Input:  geometry -  with an array of planes. each plane has its own absorption coefficient
            plane_mc_alpha - the monte carlo population for each plane
            jmc - which monte carlo individual
    Output: parsed_geometry
    '''
    for jp in np.arange(0, len(geometry.planes)):
        geometry.planes[jp].alpha = plane_mc_alpha[jp][jmc]
    return geometry


