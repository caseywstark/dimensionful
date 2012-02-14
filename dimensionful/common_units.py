"""

Define the common units, in the array of powers form.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

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
dyne = Unit("dyne")
erg  = Unit("erg")
esu  = Unit("esu")

# SI stuff
m = Unit("m")

# times
minute = Unit("min")  # can't use `min` because of Python keyword :(
hr = Unit("hr")
day = Unit("day")
yr = Unit("yr")

# solar units
Msun = Unit("Msun")
Rsun = Unit("Rsun")
Lsun = Unit("Lsun")
Tsum = Unit("Tsun")

# astro distances
AU = Unit("AU")
pc = Unit("pc")
ly = Unit("ly")
