import numpy as np
import matplotlib.pyplot as plt
#from room import Geometry, GeometryMat

class StatisticalMat():
    def __init__(self,geometry, freq, c0, air_absorption):
        self.volume = geometry.volume
        self.total_area = geometry.total_area
        self.freq = freq
        self.c0 = c0
        self.air_absorption = np.array(air_absorption)

        # Whole room
        no_planes = len(geometry.planes)
        no_alphas = len(geometry.planes[0].alpha)
        planes_areas = np.zeros((no_planes,))
        planes_alpha_mtx = np.zeros((no_planes, no_alphas))
        # x, y, z
        dot_normal_x = np.zeros((no_planes,))
        dot_normal_y = np.zeros((no_planes,))
        dot_normal_z = np.zeros((no_planes,))

        for jp, plane in enumerate(geometry.planes):
            planes_areas[jp] = plane.area
            planes_alpha_mtx[jp] = plane.alpha
            # planes_alphaMS_mtx[jp] = np.log(1-plane.alpha  
            dot_normal_x[jp] = np.abs(np.dot(plane.normal, [1, 0, 0]))
            dot_normal_y[jp] = np.abs(np.dot(plane.normal, [0, 1, 0]))
            dot_normal_z[jp] = np.abs(np.dot(plane.normal, [0, 0, 1]))

        alphas_mtx_or = np.array(planes_alpha_mtx, dtype = np.float32)
        self.alphas_mtx = np.transpose(alphas_mtx_or)
        # mean absorption of the whole room
        aisi = planes_areas @ planes_alpha_mtx
        aisiMS = -planes_areas @ np.log(1-planes_alpha_mtx)
        self.alpha_sabine = aisi / self.total_area
        self.alpha_ms = aisiMS / self.total_area

        # mean absorption of x, y, z    
        self.sxi = planes_areas * dot_normal_x
        self.syi = planes_areas * dot_normal_y
        self.szi = planes_areas * dot_normal_z
        
        self.alpha_x = -np.log(1-(self.sxi @ planes_alpha_mtx) / np.sum(self.sxi))
        self.alpha_y = -np.log(1-(self.syi @ planes_alpha_mtx) / np.sum(self.syi))
        self.alpha_z = -np.log(1-(self.szi @ planes_alpha_mtx) / np.sum(self.szi))

        
        # Initialize RT
        # no_freq = len(self.freq)
        self.t60_s = np.array([]) #np.zeros((no_freq,))
        self.t60_e = np.array([]) 
        self.t60_k = np.array([]) 
        self.t60_ms = np.array([])
        self.t60_ap = np.array([]) 
        self.t60_fitz = np.array([]) 


    def t60_sabine(self):
        '''Sabine's reverberation time.'''
        self.t60_s = ((24.0 / np.log10(np.exp(1))) / self.c0 \
            * self.volume) / (self.total_area * self.alpha_sabine \
            + 4 * self.air_absorption * self.volume)        
        return self.t60_s
    
    def t60_eyring(self):
        '''Eyring's reverberation time.  '''
        self.t60_e = ((24.0 / np.log10(np.exp(1))) / self.c0 \
            * self.volume) / (-self.total_area * np.log(1-self.alpha_sabine) \
            + 4 * self.air_absorption * self.volume)        
        return self.t60_e

    def t60_kutruff(self, gamma):
        '''Kuttruff's reverberation time.'''
        # Mean absorption Kutruff
        self.alpha_k = -np.log(1-self.alpha_sabine) * \
            (1.0 + 0.5 * gamma**2 * np.log(1-self.alpha_sabine))

        # RT
        self.t60_k = ((24.0 / np.log10(np.exp(1))) / self.c0 \
            * self.volume) / (self.total_area * self.alpha_k \
            + 4 * self.air_absorption * self.volume)        
        return self.t60_k
    
    def t60_milsette(self):
        '''Millington-Sette reverberation time.'''
        # RT
        self.t60_ms = ((24.0 / np.log10(np.exp(1))) / self.c0 \
            * self.volume) / (self.total_area * self.alpha_ms \
            + 4 * self.air_absorption * self.volume)        
        return self.t60_ms
    
    def t60_araup(self):
        '''Arau Puchades reverberation time.'''
        # Mean absorption Arau-Puchades
        self.alpha_ap = self.alpha_x**(np.sum(self.sxi) / self.total_area) \
        * self.alpha_y**(np.sum(self.syi) / self.total_area) \
        * self.alpha_z**(np.sum(self.szi) / self.total_area)

        # RT
        self.t60_ap = ((24.0 / np.log10(np.exp(1))) / self.c0 \
            * self.volume) / (self.total_area * self.alpha_ap \
            + 4 * self.air_absorption * self.volume)        
        return self.t60_ap

    def t60_fitzroy(self):
        '''Arau Puchades reverberation time.'''
        # Mean absorption Arau-Puchades
        self.alpha_fitz = self.total_area * self.alpha_x * self.alpha_y * self.alpha_z \
            / (np.sum(self.sxi) * self.alpha_y * self.alpha_z + \
            np.sum(self.syi) * self.alpha_x * self.alpha_z + \
            np.sum(self.szi) * self.alpha_x * self.alpha_y)

        # RT
        self.t60_fitz = ((24.0 / np.log10(np.exp(1))) / self.c0 \
            * self.volume) / (self.total_area * self.alpha_fitz \
            + 4 * self.air_absorption * self.volume)        
        return self.t60_fitz

    def plot_t60(self):
        '''
        Plot the reverberation time acording to statistical theory
        '''
        if (self.t60_s.size != 0 and self.t60_s.size == self.freq.size):
            plt.plot(self.freq, self.t60_s, 'bo-', label='Sabine')
        
        if (self.t60_e.size != 0 and self.t60_e.size == self.freq.size):
            plt.plot(self.freq, self.t60_e, 'ro-', label='Eyring')
        
        if (self.t60_k.size != 0 and self.t60_k.size == self.freq.size):
            plt.plot(self.freq, self.t60_k, marker='o', color='mediumvioletred', label='Kuttruff')

        if (self.t60_ms.size != 0 and self.t60_ms.size == self.freq.size):
            plt.plot(self.freq, self.t60_ms, marker='o', color='gold', label='Millington-Sette')
        
        if (self.t60_ap.size != 0 and self.t60_ap.size == self.freq.size):
            plt.plot(self.freq, self.t60_ap, 'gs-', label='Arau-Puchades')
        
        if (self.t60_fitz.size != 0 and self.t60_fitz.size == self.freq.size):
            plt.plot(self.freq, self.t60_fitz, marker='s', color='chocolate', label='Fitzroy')

        plt.grid(linestyle = '--')
        plt.xscale('log')
        plt.legend(loc = 'lower left')
        plt.xticks(self.freq, ['63', '125', '250', '500', '1000', '2000', '4000', '8000'])
        plt.show()

# , labels = ['63', '125', '250', '500', '1000', '2000', '4000', '8000']        
# def alpha_mean_sabine(geometry):
#     no_planes = len(geometry['plane'])
#     no_alphas = len(geometry['plane'][0]['alpha'])
#     planes_areas = np.zeros((no_planes,))
#     planes_alpha_mtx = np.zeros((no_planes, no_alphas))
#     for i, plane in enumerate(geometry['plane']):
#         planes_areas[i] = plane['area']
#         planes_alpha_mtx[i] = plane['alpha']

#     # mean absorption of the whole room
#     aisi = planes_areas @ planes_alpha_mtx
#     alpha = aisi / geometry['TotalArea']

#     # alpha x
#     dot_normal_x = np.zeros((no_planes,))
#     dot_normal_y = np.zeros((no_planes,))
#     dot_normal_z = np.zeros((no_planes,))
#     for i, plane in enumerate(geometry['plane']):
#         dot_normal_x[i] = np.abs(np.dot(plane['normal'], [1, 0, 0]))
#         dot_normal_y[i] = np.abs(np.dot(plane['normal'], [0, 1, 0]))
#         dot_normal_z[i] = np.abs(np.dot(plane['normal'], [0, 0, 1]))

#     sxi = planes_areas * dot_normal_x
#     syi = planes_areas * dot_normal_y
#     szi = planes_areas * dot_normal_z

#     alpha_x = (sxi @ planes_alpha_mtx) / np.sum(sxi)
#     alpha_y = (syi @ planes_alpha_mtx) / np.sum(syi)
#     alpha_z = (szi @ planes_alpha_mtx) / np.sum(szi)

#     # mean alpha
#     alpha_ap = alpha_x**(np.sum(sxi) / geometry['TotalArea']) \
#         * alpha_y**(np.sum(syi) / geometry['TotalArea']) \
#         * alpha_z**(np.sum(szi) / geometry['TotalArea'])

#     return alpha, alpha_ap


# def t60s(geometry, general, alphamean):
#     '''Sabine'''
#     return ((24.0 / np.log10(np.exp(1))) / general['air']['c0'] \
#         * geometry['Volume']) / (geometry['TotalArea'] * alphamean \
#         + 4 * general['air']['m'] * geometry['Volume'])


# def t60e(geometry, general, alphamean):
#     '''Eyring'''
#     return ((24.0 / np.log10(np.exp(1))) / general['air']['c0'] \
#         * geometry['Volume']) / (-geometry['TotalArea'] * np.log(1-alphamean) \
#         + 4 * general['air']['m'] * geometry['Volume'])


# def t60ap(geometry, general, alphamean_ap):
#     '''Arau-Puchades'''
#     return ((24.0 / np.log10(np.exp(1))) / general['air']['c0'] \
#         * geometry['Volume']) / (-geometry['TotalArea'] * np.log(1-alphamean_ap) \
#         + 4 * general['air']['m'] * geometry['Volume'])
