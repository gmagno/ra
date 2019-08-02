import numpy as np
import matplotlib.pyplot as plt
import itertools
import time
import ra_cpp

def process_results(Dt, ht_length, freq, sources, receivers):
    print("processing results...")
    time_bins = np.arange(0.0, 1.2 * ht_length, Dt)
    sou = []
    for s in sources:
        rec = [] #SRPairRec()
        for jrec, r in enumerate(receivers):
            rec.append(RecResults(s, jrec, time_bins, freq))
        sou.append(SouResults(rec, time_bins, freq))
    return sou
            # # concatenate time_crosses - out of order
            # time_cat = np.array(concatenate_tarray(
            #     jrec, s.rays, s.reccrossdir[jrec].time_dir), dtype = np.float32)
            # # sort time vector
            # id_sorted_time = np.argsort(time_cat)
            # time_sorted = time_cat[id_sorted_time]
            # # concatenate sound intensities
            # intensity_cat = np.array(concatenate_iarray(
            #     jrec, s.rays, s.reccrossdir[jrec].i_dir), dtype = np.float32)
            # # sort intensity
            # intensity_sorted = intensity_cat[:, id_sorted_time]
            # results = Results()
            # results.reflectogram_hist(time_bins, time_sorted, intensity_sorted[0,:])
    # print(sou.a)
            # print(intensity_sorted[0,:])
    # plt.plot(time_sorted, 10 * np.log10(intensity_sorted[0,:]/np.max(intensity_sorted[0,:])), '-')
    # plt.plot(time_sorted, np.log10(intensity_sorted[0,:]), '-k')
    # plt.plot(time_bins, np.log10(results.reflecto[:-1]), '-r')
    # plt.grid(linestyle = '-')
    # plt.stem(time_sorted, 10* np.log10(intensity_sorted/np.amax(intensity_sorted)), markerfmt= ' ', bottom=-80, use_line_collection=True)
    
    # plt.stem(time_bins, 10* np.log10(rec.reflectogram[:-1]/np.amax(rec.reflectogram[:-1])),
    #     markerfmt= ' ', bottom=-80, use_line_collection=True)
    # plt.ylim((-80, 10))
    # plt.show()
    # print(np.log10(results.reflecto[:-1]))

class RecResults(object):
    def __init__(self, source, jrec, time_bins, freq):
        # concatenate time_crosses - out of order
        # start_time = time.time()
        # time_cat = np.array(concatenate_tarray(
        #     jrec, source.rays, source.reccrossdir[jrec].time_dir), dtype = np.float32)
        # print(" {} seconds to concatenate time (py).".format(time.time() - start_time))
        start_time = time.time()
        time_cat = np.array(ra_cpp._time_cat(
            source.rays, source.reccrossdir[jrec].time_dir, jrec), dtype = np.float32)
        print(" {} seconds to concatenate time (c++).".format(time.time() - start_time))
        # print("Py time: {}".format(time_cat[0:10]))
        # print("C++ time: {}".format(time_catc[0:10]))
        # sort time vector
        id_sorted_time = np.argsort(time_cat)
        time_sorted = time_cat[id_sorted_time]
        # concatenate sound intensities
        # start_time = time.time()
        # intensity_cat = np.array(concatenate_iarray(
        #     jrec, source.rays, source.reccrossdir[jrec].i_dir), dtype = np.float32)
        # print(" {} seconds to concatenate intensity (py).".format(time.time() - start_time))

        # print(source.reccrossdir[jrec].i_dir.shape)
        start_time = time.time()
        intensity_cat = np.array(ra_cpp._intensity_cat(
            source.rays, source.reccrossdir[jrec].i_dir,
            jrec, time_cat.size), dtype = np.float32)
        print(" {} seconds to concatenate intensity (c++).".format(time.time() - start_time))
        # print("Py intensity: {}".format(intensity_cat[:,0:4]))
        # print("C++ intensity: {}".format(intensity_catc[:,0:4]))
        
        # sort intensity
        intensity_sorted = intensity_cat[:, id_sorted_time]
        # reflectogram
        self.reflectogram = reflectogram_hist(time_bins, time_sorted, intensity_sorted)
        self.decay = decay_curve(self.reflectogram)
        # Calculate the direct sound id
        direct_sound_idarr = np.nonzero(self.reflectogram[0,:])
        id_dir = direct_sound_idarr[0]
        # print(np.shape(direct_sound_idarr))
        # T20
        # print("id of direct sound {}".format(id_dir))
        # plt.scatter(id_dir, id_dir)
        # plt.show()
        self.EDT = edt(time_bins, self.decay, id_dir[0], freq)
        self.T20 = t20(time_bins, self.decay, id_dir[0], freq)
        self.T30 = t30(time_bins, self.decay, id_dir[0], freq)
        self.C80 = c80(time_bins, self.reflectogram, id_dir[0], freq)
        self.D50 = d50(time_bins, self.reflectogram, id_dir[0], freq)
        self.Ts = ts(time_bins, self.reflectogram, id_dir[0], freq)
        self.G = g_db(self.reflectogram, source.power_lin, freq)


def reflectogram_hist(time_bins, time_sorted, intensity_sorted):
    bins = np.digitize(time_sorted, time_bins)
    reflectogram = np.bincount(bins, weights = intensity_sorted[0,:])
    for i_freq in intensity_sorted[1:,:]:
        ref = np.bincount(bins, weights = i_freq)
        reflectogram = np.vstack((reflectogram, ref))
    # reflecto = np.bincount(bins, weights = intensity_sorted)
    return reflectogram[:,:-1]

def decay_curve(reflectogram):
    '''
    This function is used to calculate the decay of a source-receiver pair
    '''
    # first band
    reverse_reflecto = reflectogram[0,::-1]
    decay = np.cumsum(reverse_reflecto)[::-1]
    # other bands
    for r_freq in reflectogram[1:,:]:
        reverse_reflecto = r_freq[::-1]
        decay = np.vstack((decay, np.cumsum(reverse_reflecto)[::-1]))
    return decay

def edt(time, decay, id_dir, freq):
    '''
    This function is used to calculate EDT by curve fitting the decay from 0 dB to -10dB
    '''
    ## The next two lines get direct sound without any information from source and receiver
    EDT = np.zeros(freq.size, dtype = np.float32)
    jf = 0
    for jdec, dec in enumerate(decay):
        np.seterr(divide = 'ignore')
        decdB = 10 * np.log10(dec[id_dir:]/
            np.amax(dec[id_dir:]))
        # print(time.shape)
        id_to_fit = np.where((decdB < 0.0) & (decdB > -10.0))
        try:
            p = np.polyfit(time[id_to_fit], decdB[id_to_fit], 1)
            EDT[jdec] = -60 / p[0]
        except:
            print("I could not calculate EDT for the {}.".format(freq[jf])+
                "[Hz] frequency band. Try to use more rays or"+
                "extend the length of h(t) of the simmulation.")
        jf=+1
    return EDT

def t20(time, decay, id_dir, freq):
    '''
    This function is used to calculate T20 by curve fitting the decay from -5 dB to -25dB
    '''
    ## The next two lines get direct sound without any information from source and receiver
    T20 = np.zeros(freq.size, dtype = np.float32)
    jf = 0
    for jdec, dec in enumerate(decay):
        np.seterr(divide = 'ignore')
        decdB = 10 * np.log10(dec[id_dir:]/
            np.amax(dec[id_dir:]))
        # print(time.shape)
        id_to_fit = np.where((decdB < -5.0) & (decdB > -25.0))
        try:
            p = np.polyfit(time[id_to_fit], decdB[id_to_fit], 1)
            T20[jdec] = -60 / p[0]
        except:
            print("I could not calculate T20 for the {}.".format(freq[jf])+
                "[Hz] frequency band. Try to use more rays or"+
                "extend the length of h(t) of the simmulation.")
        jf=+1
    return T20

def t30(time, decay, id_dir, freq):
    '''
    This function is used to calculate T30 by curve fitting the decay from -5 dB to -25dB
    '''
    ## The next two lines get direct sound without any information from source and receiver
    T30 = np.zeros(freq.size, dtype = np.float32)
    jf = 0
    for jdec, dec in enumerate(decay):
        np.seterr(divide = 'ignore')
        decdB = 10 * np.log10(dec[id_dir:]/
            np.amax(dec[id_dir:]))
        # print(time.shape)
        id_to_fit = np.where((decdB < -5.0) & (decdB > -35.0))
        try:
            p = np.polyfit(time[id_to_fit], decdB[id_to_fit], 1)
            T30[jdec] = -60 / p[0]
        except:
            print("I could not calculate T30 for the {}.".format(freq[jf])+
                "[Hz] frequency band. Try to use more rays or"+
                "extend the length of h(t) of the simmulation.")
        jf=+1
    return T30

def c80(time, reflectogram, id_dir, freq):
    '''
    This function is used to calculate T30 by curve fitting the decay from -5 dB to -25dB
    '''
    ## The next two lines get direct sound without any information from source and receiver
    C80 = np.zeros(freq.size, dtype = np.float32) - np.inf
    jf = 0
    for jref, ref in enumerate(reflectogram):
        np.seterr(divide = 'ignore')
        try:
            id_to_sum = np.where(time <= 0.080 + time[id_dir])
            C80[jref] = 10 * np.log10(np.sum(ref[id_to_sum[0]]) / np.sum(ref[id_to_sum[0][-1]+1:]))
        except:
            print("I could not calculate C80 for the {}.".format(freq[jf])+
                "[Hz] frequency band. Try to use more rays or"+
                "extend the length of h(t) of the simmulation.")
        jf=+1
    return C80

def d50(time, reflectogram, id_dir, freq):
    '''
    This function is used to calculate T30 by curve fitting the decay from -5 dB to -25dB
    '''
    ## The next two lines get direct sound without any information from source and receiver
    D50 = np.zeros(freq.size, dtype = np.float32)-0.1
    jf = 0
    for jref, ref in enumerate(reflectogram):
        np.seterr(divide = 'ignore')
        try:
            id_to_sum = np.where(time <= 0.050 + time[id_dir])
            D50[jref] = 100 * np.sum(ref[id_to_sum[0]]) / np.sum(ref)
        except:
            print("I could not calculate D50 for the {}.".format(freq[jf])+
                "[Hz] frequency band. Try to use more rays or"+
                "extend the length of h(t) of the simmulation.")
        jf=+1
    return D50

def ts(time, reflectogram, id_dir, freq):
    '''
    This function is used to calculate T30 by curve fitting the decay from -5 dB to -25dB
    '''
    ## The next two lines get direct sound without any information from source and receiver
    Ts = np.zeros(freq.size, dtype = np.float32)
    jf = 0
    for jref, ref in enumerate(reflectogram):
        np.seterr(divide = 'ignore')
        try:
            Ts[jref] = np.sum(np.multiply(time, ref))/np.sum(ref) - time[id_dir]
        except:
            print("I could not calculate Ts for the {}.".format(freq[jf])+
                "[Hz] frequency band. Try to use more rays or"+
                "extend the length of h(t) of the simmulation.")
        jf=+1
    return Ts

def g_db(reflectogram, Wlin, freq):
    '''
    This function is used to calculate T30 by curve fitting the decay from -5 dB to -25dB
    '''
    ## The next two lines get direct sound without any information from source and receiver
    G = np.zeros(freq.size, dtype = np.float32) - np.inf
    jf = 0
    for jref, ref in enumerate(reflectogram):
        np.seterr(divide = 'ignore')
        try:
            G[jref] = 10.0 * np.log10(np.sum(ref)) -\
                10.0 * np.log10(Wlin[jref] / (4.0 * np.pi * 100.0))
        except:
            print("I could not calculate G for the {}.".format(freq[jf])+
                "[Hz] frequency band. Try to use more rays or"+
                "extend the length of h(t) of the simmulation.")
        jf=+1
    return G

###########################################################
def concatenate_tarray(jrec, srays, time_dir):
    time_cat = []
    time_cat.append(time_dir)
    for ray in srays:
        time_cross = ray.recs[jrec].time_cross
        time_cat.extend(time_cross)
    return time_cat

def concatenate_iarray(jrec, srays, i_dir):
    intensity_cat = []
    intensity_cat = np.array(i_dir, dtype = np.float32) # np.zeros((8,1), dtype = np.float32)#
    intensity_cat = intensity_cat.reshape(len(i_dir),1)
    for ray in srays:
        i_cross = np.array(ray.recs[jrec].i_cross, dtype = np.float32)
        intensity_cat = np.hstack((intensity_cat, i_cross))
    return intensity_cat

class SouResults(object):
    def __init__(self, recdata, time, freq):
        self.rec = recdata
        self.time = time
        self.freq = freq

    def plot_single_reflecrogram(self, band = 0, jrec = 0):
        '''
        Plots a single reflectogram and decay curve.
        inputs: band - index of the frequency band to plot
                js - index of the source
                jrec - index of the receiver
        outputs: void
        '''
        np.seterr(divide = 'ignore')
        title = 'Reflectogram and decay for receiver ' + str(jrec) +\
            ' at ' + str(self.freq[band]) + ' [Hz]'
        legend = str(self.freq[band]) + ' [Hz]'
        reflecto = 10 * np.log10(self.rec[jrec].reflectogram[band,:]/
            np.amax(self.rec[jrec].reflectogram[band,:]))
        decay = 10 * np.log10(self.rec[jrec].decay[band,:]/
            np.amax(self.rec[jrec].decay[band,:]))
        plt.stem(self.time, reflecto, markerfmt= ' ',
            bottom=-80, use_line_collection=True, label = 'reflectogram')
        plt.plot(self.time, decay, 'k', label = 'decay, '+legend)
        plt.legend(loc = 'upper right')
        plt.title(title)
        plt.grid(linestyle = '--')
        plt.xlabel('Time [s]')
        plt.ylabel('Intensity [dB]')
        plt.ylim((-80, 10))
        plt.show()

    def plot_decays(self, jrec = 0):
        '''
        Plots a single reflectogram and decay curve.
        inputs: band - index of the frequency band to plot
                js - index of the source
                jrec - index of the receiver
        outputs: void
        '''
        np.seterr(divide = 'ignore')
        for band, f in enumerate(self.freq):
            legend = str(f) + ' [Hz]'
            decay = 10 * np.log10(self.rec[jrec].decay[band,:]/
                np.amax(self.rec[jrec].decay[band,:]))
            plt.plot(self.time, decay, label = legend)
        plt.legend(loc = 'upper right')
        plt.grid(linestyle = '--')
        plt.xlabel('Time [s]')
        plt.ylabel('Intensity [dB]')
        plt.ylim((-80, 10))
        plt.show()

    def plot_edt(self, ht_max = 3.0):
        '''
        Plots the EDT for all receivers for a given sound source.
        outputs: void
        '''
        for jrec, r in enumerate(self.rec):
            legend = 'receiver ' + str(jrec+1)
            plt.plot(self.freq, r.EDT, label = legend)
        plt.grid(linestyle = '--')
        plt.xscale('log')
        plt.legend(loc = 'lower left')
        plt.title('EDT')
        plt.xticks(self.freq, ['63', '125', '250', '500', '1000', '2000', '4000', '8000'])
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('EDT [s]')
        plt.ylim((0, 1.5*ht_max))
        plt.show()

    def plot_t20(self, ht_max = 3.0):
        '''
        Plots the T20 for all receivers for a given sound source.
        outputs: void
        '''
        for jrec, r in enumerate(self.rec):
            legend = 'receiver ' + str(jrec+1)
            plt.plot(self.freq, r.T20, label = legend)
        plt.grid(linestyle = '--')
        plt.xscale('log')
        plt.legend(loc = 'lower left')
        plt.title('T20')
        plt.xticks(self.freq, ['63', '125', '250', '500', '1000', '2000', '4000', '8000'])
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('T20 [s]')
        plt.ylim((0, ht_max))
        plt.show()

    def plot_t30(self, ht_max = 3.0):
        '''
        Plots the T30 for all receivers for a given sound source.
        outputs: void
        '''
        for jrec, r in enumerate(self.rec):
            legend = 'receiver ' + str(jrec+1)
            plt.plot(self.freq, r.T30, label = legend)
        plt.grid(linestyle = '--')
        plt.xscale('log')
        plt.legend(loc = 'lower left')
        plt.title('T30')
        plt.xticks(self.freq, ['63', '125', '250', '500', '1000', '2000', '4000', '8000'])
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('T30 [s]')
        plt.ylim((0, ht_max))
        plt.show()

    def plot_c80(self):
        '''
        Plots the C80 for all receivers for a given sound source.
        outputs: void
        '''
        for jrec, r in enumerate(self.rec):
            legend = 'receiver ' + str(jrec+1)
            plt.plot(self.freq, r.C80, label = legend)
        plt.grid(linestyle = '--')
        plt.xscale('log')
        plt.legend(loc = 'lower right')
        plt.title('C80')
        plt.xticks(self.freq, ['63', '125', '250', '500', '1000', '2000', '4000', '8000'])
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('C80 [dB]')
        # plt.ylim((0, ht_max))
        plt.show()

    def plot_d50(self):
        '''
        Plots the T20 for all receivers for a given sound source.
        outputs: void
        '''
        for jrec, r in enumerate(self.rec):
            legend = 'receiver ' + str(jrec+1)
            plt.plot(self.freq, r.D50, label = legend)
        plt.grid(linestyle = '--')
        plt.xscale('log')
        plt.legend(loc = 'lower right')
        plt.title('D50')
        plt.xticks(self.freq, ['63', '125', '250', '500', '1000', '2000', '4000', '8000'])
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('D50 [%]')
        # plt.ylim((0, ht_max))
        plt.show()

    def plot_ts(self):
        '''
        Plots the Ts for all receivers for a given sound source.
        outputs: void
        '''
        for jrec, r in enumerate(self.rec):
            legend = 'receiver ' + str(jrec+1)
            plt.plot(self.freq, 1000 * r.Ts, label = legend)
        plt.grid(linestyle = '--')
        plt.xscale('log')
        plt.legend(loc = 'best')
        plt.title('Ts')
        plt.xticks(self.freq, ['63', '125', '250', '500', '1000', '2000', '4000', '8000'])
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Ts [ms]')
        # plt.ylim((0, ht_max))
        plt.show()

    def plot_g(self):
        '''
        Plots the Ts for all receivers for a given sound source.
        outputs: void
        '''
        for jrec, r in enumerate(self.rec):
            legend = 'receiver ' + str(jrec+1)
            plt.plot(self.freq, r.G, label = legend)
        plt.grid(linestyle = '--')
        plt.xscale('log')
        plt.legend(loc = 'best')
        plt.title('G')
        plt.xticks(self.freq, ['63', '125', '250', '500', '1000', '2000', '4000', '8000'])
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('G [dB]')
        # plt.ylim((0, ht_max))
        plt.show()

# class SRPairs():
#     def __init__(self, Dt, ht_length, freq):
#         # time histogram
#         self.time = np.arange(0.0, 1.2 * ht_length, Dt)
#         # frequency bands
#         self.freq = freq

#     def reflectogram(self, sources, receivers):
#         '''
#         Calculate the reflectogram for each source-receiver pair
#         '''
#         sou = []
#         for s in sources:
#             rec = [] #SRPairRec()
#             for jrec, r in enumerate(receivers):
#                 # concatenate time_crosses - out of order
#                 time_cat = np.array(concatenate_tarray(
#                     jrec, s.rays, s.reccrossdir[jrec].time_dir), dtype = np.float32)
#                 # sort time vector
#                 id_sorted_time = np.argsort(time_cat)
#                 time_sorted = time_cat[id_sorted_time]
#                 # concatenate sound intensities
#                 intensity_cat = np.array(concatenate_iarray(
#                     jrec, s.rays, s.reccrossdir[jrec].i_dir), dtype = np.float32)
#                 # sort intensity
#                 intensity_sorted = intensity_cat[:, id_sorted_time]
#                 recobj = SRPairRec()
#                 rec.append(recobj)
#             sou.append(rec)
#         print("Object created - testing")
        
                # recobj.reflecto_histogram(self.time,
                #     time_sorted, intensity_sorted)
                # print(recobj.reflectogram)
                # id_sorted_time = np.argsort(time_flat)
                # self.time = time_flat[id_sorted_time]

# class SRPairRec():
#     def __init__(self, reflectogram = [], decay = []):
#         self.reflectogram = np.array(reflectogram, dtype = np.float32)
#         self.decay = np.array(decay, dtype = np.float32)

    # def reflecto_histogram(self, time_bins, time_sorted, intensity_sorted):
    #     bins = np.digitize(time_sorted, time_bins)
    #     print(intensity_sorted.size)
    #     reflecto_jf = np.bincount(bins, weights = intensity_sorted[0,:])
    #     self.reflectogram = reflecto_jf
        # print(self.reflectogram[0:3])
        # for row in intensity_sorted:
        #     i_freq = row
        #     # print(row)
        #     reflecto_jf = np.bincount(bins, weights = intensity_sorted[0])
        #     print(reflecto_jf)
        #     self.reflectogram = np.hstack((self.reflectogram, reflecto_jf))
        # self.time_bins = time_bins[0:len(self.reflecto)]

# class ReflectoAndDecay():
#     '''
#     Class to calculate the reflectogram and decay curve from geometrical acoustics
#     simulation

#     Input: Part of the ray tracing main data including: time instant and sound intensity
#     each time the ray hits a receiver for a given source.

#     Output: Reflectograms and decay curves for each source - receiver pair and for
#     each frequency band
#     '''
#     def __init__(self, time, intensity, freq_bands):
#         # frequency bands
#         self.freq_bands = freq_bands
        
#         # time data sorted
#         time_flat = np.array(concatenate_tarray_matlab(time))
#         id_sorted_time = np.argsort(time_flat)
#         self.time = time_flat[id_sorted_time]
        
#         # intensity data sorted accordind to time array
#         intensity_flat = np.array(concatenate_iarray_matlab(intensity,0)) # second element in input is the index of freq band loop later
#         self.intensity = intensity_flat[id_sorted_time]
#         # for jf in np.arange(len(self.freq_bands)-1):
#         #     intensity_flat = np.array(concatenate_iarray_matlab(intensity,jf)) # second element in input is the index of freq band loop later
#         #     self.intensity = intensity_flat[id_sorted_time]

#         print('reflectogram object created')

#     def reflecto_hist(self, dt, htlength):
#         time_bins = np.arange(0.0, 1.2*htlength, dt)
#         bins = np.digitize(self.time, time_bins)
#         self.reflecto = np.bincount(bins, weights = self.intensity)
#         self.time_bins = time_bins[0:len(self.reflecto)]
#         # reflecto_dB = 10*np.log10(self.reflecto/np.amax(self.reflecto))
#         # reflecto_dB = np.where(reflecto_dB == -np.inf, -1000.0, reflecto_dB)

#         # plt.stem(self.time_bins, reflecto_dB, markerfmt= ' ', bottom=-80)
#         # plt.ylim((-80, 10))
#         # plt.show()

#     def decay_curve(self):
#         reverse_reflecto = self.reflecto[::-1]
#         self.decay = np.cumsum(reverse_reflecto)[::-1]
        
#     def plot_reflecto(self, htlength):
#         '''
#         This function serves the purpose to plot reflectogram and the decay curve
#         '''
#         plt.stem(self.time_bins, 10* np.log10(self.reflecto/np.amax(self.reflecto)), markerfmt= ' ', bottom=-80)
#         plt.plot(self.time_bins, 10* np.log10(self.decay/np.amax(self.decay)), 'k')
#         plt.ylim((-80, 10))
#         plt.xlim(0, htlength)
#         plt.show()

# def concatenate_tarray_matlab(array):
#     flat_array = []
#     for i in array:
#         for j in i:
#             for k in j:
#                 flat_array.append(k)
#     return flat_array

# def concatenate_iarray_matlab(array,band):
#     flat_array_of_arrays = []
#     flat_array = []
#     for i in array: # search all elements in the array
#         flat_array_of_arrays.append(i)

#     for j in flat_array_of_arrays:
#         for k in j[band]: # loop in that frequency band
#             flat_array.append(k)
#     return flat_array




