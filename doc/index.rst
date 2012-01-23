Dimensionful Docs
=================

Some extra documentation to dimensionful. The package is pretty small, so if you
aren't sure about something, don't be too afraid to browse the source.


Example
-------

>>> import numpy as np
>>> from dimensionful.units import Unit
>>> from dimensionful.quantity import Quantity
>>>
>>> force_units = Unit("g cm s^-2")
>>> force_data = np.random.random(4)
>>> force_a = Quantity(force_data, force_units)
>>>
>>> distance_data = np.random.random(4)
>>> distance_a = Quantity(distance_data, "cm")
>>>
>>> energy_a = force_a * distance_a
>>> energy_a


Design
------

A Unit is an object with dimensions and a reference value. For now, we just use
the ``conversion_factor`` attribute to store the conversion to cgs values (of
whatever dimension).

A Quantity is an object with dimensions, a reference value, and data. The data
is completely arbitrary.

There are several ways to create units and quantities.

Units created with a symbol string: Dimensionful translates a string of
space-delimited unit symbols into the proper dimensions and conversions to CGS.

    >>> Unit("cm s^-1")
        cm s^-1
    >>> Unit("pc Myr^-1")
        pc Myr^-1

Units created with an array of powers: You can create units by specifying the
power of base units with an array-like.

    >>> Unit((1, 1, -1, 0))
        g cm s^-1
    >>> Unit(numpy.array((1, 1, -1, 0)))
        g cm s^-1

You create quantities with any data you want as the first argument and the units
as the second argument. You can pass a unit object as the units argument, or use
a string or array as above (these are passed on to the Unit constructor).

    >>> speed_unit = Unit("m s^-1")
    >>> Quantity(3.0e8, speed_unit)
        3.0e+08 m s^-1
    >>> Quantity(3.0e8, "m s^-1")  # equivalent
        3.0e+08 m s^-1
    >>> Quantity(3.0e8, (0, 1, -1, 0))  # not the same! base units are cgs so...
        3.0e+08 cm s^-1

Note that a quantity object with a single-valued ``data`` attribute is
equivalent to a unit object with a ``conversion_factor`` attribute of the same
value.


Code layout
-----------

Just some notes to give developers an idea of where to hack on things.


``dimensionful/common_units``
+++++++++++++++++++++++++++++

More of a data store for possible unit definitions. We use ``unit_symbols_dict``
for symbol lookup when creating units, and ``unit_prefixes`` for prefix lookup.


``dimensionful/constants``
++++++++++++++++++++++++++

Another data store like file. This one holds Unit objects that are typically
thought of as "constants" in science and engineering.


``dimensionful/quantity``
+++++++++++++++++++++++++

Holds the Quantity class.


``dimensionful/units``
++++++++++++++++++++++

Holds some library definitions (number of base units and fixed order), utils,
and the Unit class.


``example/*``
+++++++++++++

More-than-one-liner examples. Helpful scripts for users, hopefully.


``test/test_quantity``
++++++++++++++++++++++

Check that quantities work.


``test/test_units``
+++++++++++++++++++

Check that units work.


``test/utils``
++++++++++++++

Contains a simple function to compare two numbers up to given precision. I do
not know why this is not included in common Python test frameworks...


``setup.py``
++++++++++++

Distutils setup script.
