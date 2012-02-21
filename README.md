Dimensionful
============

A simple library for making your data dimensionful.

Install
-------

Dimensionful depends on sympy-0.71+. Please install (or upgrade) sympy first.

    $ pip install sympy

If you do not have pip in your current environment, I recommend installing it
with ``easy_install pip``.

Then install dimensionful.

    $ cd dimensionful
    $ python setup.py install

I'm looking into putting the project on pypi. In the meantime, please use the
normal distutils installer in `setup.py`.

Example
-------

This prints "The force of gravity between the Earth and Sun is
3.54296304519e+27 cm*g/s**2".

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
    print "The force of gravity between the Earth and Sun is %s" % force_gravity

You can also find this in the `example` directory.

Documentation
-------------

Some simple docs are in `dimensionful/doc`.
