"""

Physical constants.

Copyright 2012, Casey W. Stark.

"""

import numpy as np

from units import *
from quantity import Quantity

# lengths
AU = Quantity(1.49598e13, "cm")
pc = Quantity(3.08568025e18, "cm")
ly = Quantity(9.4605284e17, "cm")

# speed of light
c = Quantity(2.99792458e10, "cm s^-1")

# Gravitational constant
G = Quantity(6.673e-8, "cm^3 g^-1 s^-2")

# Boltzmann constant
k = Quantity(1.38064e-16, "erg K^1")

# Planck constant
h = Quantity(6.626070e-27, "erg s")
hbar = h / (2 * np.pi)
