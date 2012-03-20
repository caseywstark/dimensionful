"""

Physical constants in cgs.

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
k = Quantity(1.38064e-16, erg / K)

# Planck constant
h = Quantity(6.626070e-27, erg * s)
hbar = h / (2 * np.pi)

# atomic constants
e = Quantity(4.8032068e-10, esu)
m_p = Quantity(1.672623e-24, g)
m_e = Quantity(9.109389e-28, g)
amu = Quantity(1.6605402e-24, g)

# radiation
sigma_T = Quantity(6.6524588e-25, cm**2)
sigma_SB = Quantity(5.67e-5, g * K**(-4) * s**(-3))
a = Quantity(7.5657e-15, g * K**(-4) * cm**(-1) * s**(-2))
