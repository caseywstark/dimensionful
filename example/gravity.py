"""

Compute the force of gravity between the Earth and Sun.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

"""

from dimensionful.quantity import Quantity
from dimensionful.constants import G

if __name__ == "__main__":

    # Supply the mass of Earth, mass of Sun, and the distance between.
    m1 = Quantity(5.9742e27, "g")
    m2 = Quantity(1.98892e33, "g")
    r = Quantity(1.0, "AU")

    # Calculate it
    force_gravity = G * m1 * m2 / r**2

    # Report
    print ""
    print "The force of gravity between the Earth and Sun is %s" % force_gravity
    print ""
