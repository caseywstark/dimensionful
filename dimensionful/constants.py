"""

Physical constants.

Copyright 2012, Casey W. Stark.

"""

import numpy as np

from dimensionful.common_units import *

# speed of light
c = 2.99792458e10 * cm * s**-1

# Gravitational constant
G = 6.673e-8 * cm**3 * g**-1 * s**-2

# Boltzmann constant
k = 1.38064e-16 * erg * K**1

# Planck constant
h = 6.626070e-27 * erg * s
hbar = h / (2 * np.pi)
