"""

Define the common units, in the array of powers form.

Copyright 2012, Casey W. Stark.

"""

from sympy.core import Integer

from dimensions import *
from units import Unit, unit_symbols_dict

g  = Unit("g")
cm = Unit("cm")
s  = Unit("s")
K  = Unit("K")

m = Unit("m", unit_symbols_dict["m"][0], unit_symbols_dict["m"][1])

dyne = Unit("dyne", unit_symbols_dict["dyne"][0], unit_symbols_dict["dyne"][1])
erg  = g * cm**2 * s**(-2)
esu  = (erg * cm)**(1/2)

# times
minute = 60 * s  # can't use `min` because of Python keyword :(
hr = 60 * minute
day = 24 * hr
yr = 365 * day

# solar units
Msun = 1.98892e33 * g
Rsun = 6.96e10 * cm
Lsun = 3.9e33 * erg
Tsum = 5870 * K

# astro distances
AU = 1.49598e13 * cm
pc = 3.0857e18 * cm

"""
