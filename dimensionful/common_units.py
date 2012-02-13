"""

Define the common units, in the array of powers form.

Copyright 2012, Casey W. Stark.

"""

from sympy.core import Integer

from dimensionful.dimensions import *
from dimensionful.units import Unit, unit_symbols_dict

# cgs base units
g  = Unit("g")
cm = Unit("cm")
s  = Unit("s")
K  = Unit("K")

# other cgs
dyne = Unit("dyne", g * cm * s**(-2))
erg  = Unit("erg", g * cm**2 * s**(-2))
esu  = Unit("esu", (erg * cm)**(1/2))

# SI stuff
m = Unit("m", 100 * g)

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
ly = 9.4605284e17 * cm
