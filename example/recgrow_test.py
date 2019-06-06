import numpy as np
import ra_cpp

growth_allowed = 0
trans_order = 2
ref_order = 3
rec_init = 0.1
rec_max = 1.0
rec_current = 0.1
dist_cum = 10.0
Nrays = 10000

new_radii = ra_cpp._recgrow(growth_allowed, trans_order, ref_order,
    rec_init, rec_max, rec_current, dist_cum, Nrays)

print('The new receiver radius back to python is {}!!'.format(new_radii))