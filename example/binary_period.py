"""

Compute the mass transfer rate between two stars in a binary:

$$ \frac{ \dot{P} }{ P } = 3 \dot{M_1} \frac{ M_1 - M_2 }{ M_1 M_2 } $$

P is the period of the binary, M_1 and M_2 are the masses, and dM_1 / dt is the
mass transfer rate.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

"""

# Import the Quantity class
from dimensionful import Quantity, Msun, s, day, yr

# Supply the period, change in period observed over some time, and the masses.
P = Quantity(2.49, day)
dP = Quantity(20, s)
dt = Quantity(100, yr)
M1 = Quantity(2.9, Msun)
M2 = Quantity(1.4, Msun)

# Calculate it and convert to Msun / yr
Mdot = dP * M1 * M2 / (3 * P * dt * (M1 - M2))
Mdot.convert_to(Msun / yr)

# Report
print ""
print "The mass transfer rate is %s." % Mdot
print ""

# prints "The mass transfer rate is 8.38745930223e-07 Msun/yr."
