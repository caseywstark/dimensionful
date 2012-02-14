"""

Compute the force of gravity between the Earth and Sun.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

"""

# Import the gravitational constant and the Quantity class
from dimensionful import G, Quantity

# Supply the mass of Earth, mass of Sun, and the distance between.
mass_earth = Quantity(5.9742e27, "g")
mass_sun = Quantity(1.0, "Msun")
distance = Quantity(1.0, "AU")

# Calculate it
force_gravity = G * mass_earth * mass_sun / distance**2
force_gravity.convert_to_cgs()

# Report
print ""
print "The force of gravity between the Earth and Sun is %s" % force_gravity
print ""
