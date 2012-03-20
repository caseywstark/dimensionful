"""

Define some common units, so users can import the objects directly.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

"""

from dimensionful.dimensions import *
from dimensionful.units import Unit

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

gauss = Unit("gauss")
