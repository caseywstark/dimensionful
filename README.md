Dimensionful
============

Simple system for making data dimensionful.

Example
-------

This computes the force of gravity between the Earth and Sun. Prints ``The force
of gravity between the Earth and Sun is 7.92899597305e+53 g cm s^-2``

    from dimensionful.quantity import Quantity
    from dimensionful.constants import G

    # Supply the mass of Earth, mass of Sun, and the distance between.
    m1 = Quantity(5.9742e27, "g")
    m2 = Quantity(1.98892e33, "g")
    r = Quantity(1.0, "AU")

    # Calculate it
    force_gravity = G * m1 * m2 / r**2

    # Report
    print "The force of gravity between the Earth and Sun is %s" % force_gravity


Documentation
-------------

Some simple docs are in `dimensionful/doc`.
