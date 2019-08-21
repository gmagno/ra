import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import ra_cpp

def main():
    
    v_in = np.array([1.0, 0.0, 0.0]) #
    normal = np.array([-1.0, 0.0, 0.0])
    s_s = 0.1
    ref_order = 3
    s_on_off = 1
    trans_order = 2

    v_out = ra_cpp._rayreflection(v_in, normal, s_s, ref_order, s_on_off, trans_order)
    
    print(v_out)
    
    

if __name__ == '__main__':
    main()