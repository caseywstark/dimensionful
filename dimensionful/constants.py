"""

Physical constants.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

"""

import numpy as np

from dimensionful.common_units import *
from dimensionful.quantity import Quantity

# speed of light
c = Quantity(2.99792458e10, cm / s)

# Gravitational constant
G = Quantity(6.673e-8, cm**3 * g**-1 * s**-2)

# Boltzmann constant
k = Quantity(1.38064e-16, erg * K)

# Planck constant
h = Quantity(6.626070e-27, erg * s)
hbar = h / (2 * np.pi)
