Dimensionful Docs
=================

Some extra documentation to dimensionful. The package is pretty small, so if you
aren't sure about something, don't be too afraid to browse the source.


Example
-------

>>> import numpy as np
>>> from dimensionful import Unit, Quantity
>>>
>>> force_units = Unit("g * cm * s**-2")
>>> force_data = np.random.random(4)
>>> force_a = Quantity(force_data, force_units)
>>>
>>> distance_data = np.random.random(4)
>>> distance_a = Quantity(distance_data, "cm")
>>>
>>> energy_a = force_a * distance_a
>>> energy_a
[ 0.40391448  0.44528124  0.10094044  0.00189099] cm**2*g/s**2


Design
------

A Unit is an object with dimensions and a reference value. For now, we just use
the ``cgs_value`` attribute to store the conversion to cgs values (of
whatever dimension).

A Quantity is an object with data and Unit object. The data is completely
arbitrary.

There are several ways to create units and quantities.

Units created with a symbol string: Dimensionful parses a string of symbols
into a Unit with the correct dimensions and cgs value. Expression parsing is
done by calling ``sympy.parsing.sympy_parser.parse_expr`` on the argument.

    >>> Unit("cm * s**-1")
        cm/s
    >>> Unit("pc * Myr**-1")
        pc/Myr

Dimensionful looks up the symbols in the expression to determine dimensions and
conversion factors. If it does not find the symbol in its "known" symbols, it
barfs.

    >>> Unit("aaa")
    Exception: Lookup failed. Unknown unit symbol 'aaa'. Please supply the
    dimensions and cgs value when creating this object.
    >>> from dimensionful import energy
    >>> Unit("aaa", dimensions=energy, cgs_value=42)
    aaa

Units created with a sympy expression: Works the same as the string case, but
it does not have to call ``sympy.parsing.sympy_parser.parse_expr`` to convert
it.

    >>> from sympy import Symbol
    >>> Unit(Symbol("cm") / Symbol("s"))
    cm/s

Units created from other units: Multiplying Units with each other and taking
Units to powers returns new Units.

    >>> from dimensionful import erg, s
    >>> new_unit = erg / s
    >>> new_unit.dimensions
    (length)**2*(mass)/(time)**3

You create Quantities with any data you want as the first argument and the units
as the second argument. You can pass a Unit object as the units argument, or use
a string or sympy expression as above (these are passed on to the Unit
constructor).

    >>> speed_unit = Unit("m / s")
    >>> Quantity(3.0e8, speed_unit)
        300000000.0 m/s
    >>> Quantity(3.0e8, "m / s")  # equivalent
        300000000.0 m/s


Non-Integer power warning
-------------------------

You might run into using non-integer powers of base units in your units. Here is
an example of a dimensionality with non-integer powers of base dimensions.

    >>> charge = (energy * length)**(1.0/2)
    >>> charge
    (length)**1.5*(mass)**0.5*1/(time)

This results in sympy expressions with sympy.core.numbers.Float powers. This is
perfectly fine, until you have to compare to other expressions that might have
sympy.core.numbers.Rational powers.

    >>> charge2 = sqrt(length**3) * sqrt(mass) / time
    >>> charge2
    (length)**(3/2)*sqrt((mass))/(time)

These expressions are clearly the same, but sympy won't know that.

    >>> charge == charge2
    False

When in doubt, I recommend using sympy's ``nsimplify`` function before comparing
expressions.

    >>> from sympy import nsimplify
    >>> nsimplify(charge)
    (length)**(3/2)*sqrt((mass))/(time)
    >>> nsimplify(charge) == charge2
    True


Code layout
-----------

Just some notes to give developers an idea of where to hack on things.


``dimensionful/common_units``
+++++++++++++++++++++++++++++

Creates objects of common Units. This is so they can be easily imported like,
``from dimensionful import dyne``.


``dimensionful/constants``
++++++++++++++++++++++++++

Another data store like file. This one holds Quantity objects of common physical
constants, like hbar.


``dimensionful/quantity``
+++++++++++++++++++++++++

Holds the Quantity class.


``dimensionful/units``
++++++++++++++++++++++

Holds the known units data structures, some unit util functions, and the Unit
class.


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
