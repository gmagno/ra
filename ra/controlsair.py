import numpy as np

class AlgControls():
    def __init__(self, config):
        '''
        Set up algorithm controls. The controls are several properties
        provided by the user. We get that from a toml file. The properties
        are:
        1: freq - frequency bands
        2: Nrays - Number of user supplied rays (the actual traced rays can be bigger)
        3: ht_length - estimated length of impulse response [s]
        4: Dt - Reflectogram resolution [s] (width of time bins)
        5: allow_scatteting - if 0 only specular reflections are allowed
        6: trasition_order - for reflection orders higher than transition
            order the reflection can be scattered.
            For for reflection orders lower than transition order
            the reflection will be specular.
        7: rec_radius_init - initial radius of all receivers
            (strongly recomend to use 10 cm - about a typical head size)
        8: allow_growth: if 1 receiver is allowed to grow after the
            reflection order is bigger than transition order. It grows according
            to tha ray travelled distance. If 0 the receivers will remain with
            the rec_radius_init as its size.
        9: rec_radius_final: receivers are only allowed to grow up to this limit.
        '''
        self.freq = np.array(config['freq'], dtype = np.float32)
        self.Nrays = config['Nrays']
        self.ht_length = config['ht_length']
        self.Dt = config['Dt']
        self.allow_scattering = config['allow_scattering']
        self.transition_order = config['transition_order']
        self.rec_radius_init = config['rec_radius_init']
        self.alow_growth = config['allow_growth']
        self.rec_radius_final = config['rec_radius_final']

class AirProperties():
    def __init__(self, config):
        '''
        Set up air properties. The inputs given by the user are:
        1: temperature - in Celsius
        2: hr - relative humidity [%]
        3: p_atm - atmospheric pressure
        The class can calculate the following properties according to
        standards:
        4: rho0 - air density in [kg/m^3]
        5: c0 - sound speed in air [m/s]
        6: m - air absorption coefficient
            (array of same size as controls.freq)
        '''
        self.temperature = np.array(config['Temperature'])
        self.hr = config['hr']
        self.p_atm = config['p_atm']
        temp_kelvin = self.temperature + 273.16 # temperature in [K]
        R = 287.031                 # gas constant
        rvp = 461.521               # gas constant for water vapor
        # pvp from Pierce Acoustics 1955 - pag. 555
        pvp = 0.0658 * temp_kelvin**3 - 53.7558 * temp_kelvin**2 \
            + 14703.8127 * temp_kelvin - 1345485.0465
        # Constant pressure specific heat
        cp = 4168.8 * (0.249679 - 7.55179e-5 * temp_kelvin \
            + 1.69194e-7 * temp_kelvin**2 \
            - 6.46128e-11 * temp_kelvin**3)
        cv = cp - R                 # Constant volume specific heat
        # b2 = vis * cp / kappla      # Prandtl number
        gam = cp / cv               # specific heat constant ratio
        # Air density
        self.rho0 = self.p_atm / (R * temp_kelvin) \
            - (1/R - 1/rvp) * self.hr/100 * pvp/temp_kelvin
        # Air sound speed
        self.c0 = (gam * self.p_atm/self.rho0)**0.5

    def air_absorption(self, freq):
        '''
        Calculates the air aborption coefficient in [m^-1]
        '''
        T_0 = 293.15                # Reference temperature [k]
        T_01 = 273.15               # 0 [C] in [k]
        temp_kelvin = self.temperature + 273.15 # Input temp in [k]
        patm_atm = self.p_atm / 101325 # atmosferic pressure [atm]
        F = freq / patm_atm         # relative frequency
        a_ps_ar = np.zeros(F.shape)
        # Saturation pressure
        psat = patm_atm * 10**(-6.8346 * (T_01/temp_kelvin)**1.261 \
            + 4.6151)
        h = patm_atm * self.hr *(psat/patm_atm)
        # Oxygen gas molecule (N2) relaxation frequency
        F_rO = 1/patm_atm * (24 + 4.04 * 10**4 * h * (0.02 + h) \
            / (0.391 + h))
        # Nytrogen gas molecule (N2) relaxation frequency
        F_rN = 1/patm_atm * (T_0/temp_kelvin)**(1/2) * \
            (9 + 280 * h *np.exp(-4.17 * ((T_0/temp_kelvin)**(1/3) - 1)) )
        # Air absorption in [dB/m]
        alpha_ps = 100 * F**2 / patm_atm * (1.84 \
            * 10**(-11) * (temp_kelvin/T_0)**(1/2) \
                + (temp_kelvin/T_0)**(-5/2) \
            * (0.01278 * np.exp(-2239.1/temp_kelvin) \
                / (F_rO + F**2 / F_rO) \
            + 0.1068*np.exp(-3352/temp_kelvin) / (F_rN + F**2 / F_rN)))
        a_ps_ar = alpha_ps * 20 / np.log(10)
        # Air absorption in [1/m]
        self.m = np.array((1/100) * a_ps_ar * patm_atm \
            / (10 * np.log10(np.exp(1))), dtype = np.float32)
        return self.m

####################### To save/load the simulation #########################
import pickle
def save_sim(controls = [], air = [], rays_i = [],
    geometry = [], stats_theory = [], sources = [],
    receivers = [], s_reflecto_par = [], stats_analysis = [],
    path = '/home/eric/dev/ra/data/legacy/odeon_ex/',
    fname = 'room_sim'):
    '''
    A function to save the simulation as a pickle file
    '''
    print('I am saving everything. It may take a while if the simulation is big.')
    with open(path+fname+'.pkl', 'wb') as output:
        pickle.dump(controls, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(air, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(rays_i, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(geometry, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(stats_theory, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(sources, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(receivers, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(s_reflecto_par, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(stats_analysis, output, pickle.HIGHEST_PROTOCOL)
    print('Saving is done!')

def load_sim(
    path = '/home/eric/dev/ra/data/legacy/odeon_ex/',
    fname = 'room_sim'):
    '''
    A function to load the simulation as a pickle file
    '''
    print('I am loading everything. It may take a while if the simulation is big.')
    with open(path+fname+'.pkl', 'rb') as input:
        controls = pickle.load(input)
        air = pickle.load(input)
        rays_i = pickle.load(input)
        geometry = pickle.load(input)
        stats_theory = pickle.load(input)
        sources = pickle.load(input)
        receivers = pickle.load(input)
        s_reflecto_par = pickle.load(input)
        stats_analysis = pickle.load(input)
    print('Loading is done!')
    return controls, air, rays_i, geometry, stats_theory, sources, receivers, s_reflecto_par, stats_analysis
