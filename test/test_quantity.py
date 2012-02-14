"""

Test quantity functionality.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

"""

import nose
import numpy as np

from utils import equal_sigfigs

from dimensionful.units import Unit
from dimensionful.quantity import Quantity

# @todo: global option?
required_precision = 4

def test_creation_with_unit_object():
    """
    Create a quantity object with a unit object as ``unit`` parameter.

    """
    u1 = Unit("Mpc")
    q1 = Quantity(1.0, u1)

    assert q1.data == 1.0
    assert q1.units == u1

def test_creation_with_unit_string():
    """
    Create a quantity object with a unit symbol as ``unit`` parameter.

    """
    u1 = Unit("Mpc")
    q1 = Quantity(1.0, "Mpc")

    assert q1.data == 1.0
    assert q1.units == u1

def test_string_representation():
    """
    Check how a quantity prints.

    """
    q1 = Quantity(1.0, "Mpc/yr")

    assert repr(q1) == "1.0 Mpc/yr"
    assert str(q1) == "1.0 Mpc/yr"

def test_convert_to():
    """
    Convert a density quantity from cgs to cosmological units.

    """
    u1 = Unit("g * cm**-3")
    u2 = Unit("Msun * Mpc**-3")

    q1 = Quantity(1e-29, u1)

    assert q1.units == u1

    q1.convert_to(u2)

    assert equal_sigfigs(q1.data, 1.47721e11, required_precision)
    assert q1.units == u2

# @todo: real exceptions...
def test_convert_bad_dimensions():
    """
    Get Exception from converting to wrong dimensionality.

    """
    u1 = Unit("Msun * Mpc**-2")
    q1 = Quantity(1e-29, "g * cm**-3")

    try:
        q1.convert_to(u1)
    except Exception:
        pass

def test_convert_to_cgs():
    """
    Convert a cosmological density quantity to cgs.

    """
    u1 = Unit("Msun * Mpc**-3")
    u2 = Unit("g * cm**-3")

    q1 = Quantity(1.47721e11, "Msun * Mpc**-3")

    assert q1.units == u1

    q1.convert_to_cgs()

    assert equal_sigfigs(q1.data, 1e-29, required_precision)
    assert q1.units == u2

def test_get_in():
    """
    Get a cgs density quantity in cosmological units.

    """
    u1 = Unit("g * cm**-3")
    u2 = Unit("Msun * Mpc**-3")

    q1 = Quantity(1e-29, u1)
    q2 = q1.get_in(u2)

    assert equal_sigfigs(q2.data, 1.47721e11, required_precision)
    assert q2.units == u2

def test_get_in_cgs():
    """
    Get cosmological density quantity in cgs.

    """
    u1 = Unit("Msun * Mpc**-3")
    u2 = Unit("g * cm**-3")

    q1 = Quantity(1.47721e11, u1)
    q2 = q1.get_in_cgs()

    assert equal_sigfigs(q2.data, 1e-29, required_precision)
    assert q2.units == u2

def test_addition():
    """
    Add two quantities.

    """
    q1 = Quantity(1.0, "cm * s**-1")  # plus
    q2 = Quantity(2.0, "cm * s**-1")  # equals
    q3 = Quantity(3.0, "cm * s**-1")

    q4 = Quantity(1.0, "cm")  # wrong dimension

    q5 = Quantity(1.0, "km * hr**-1")
    q6 = Quantity(.01 + 1.e3 / 3600, "m * s**-1")

    assert q1 + q2 == q3

    try:
        dim_fail = q1 + q4
    except Exception:  # @todo: real exception type
        pass

    assert q1 + q5 == q6

def test_addition_bad_dims():
    """
    Try to add two quantities of different dimension.

    """
    u1 = Unit("yr / s")  # dimensionless
    q1 = Quantity(1, u1)
    number = 4
    q2 = Quantity(1, "cm * s")
    q3 = Quantity(1, "cm * s**-1")

    q4 = q1 + number

    assert q4.data == 5
    assert q4.units == u1

    try:
        q5 = q2 + q3
    except Exception:
        pass

def test_subtraction():
    """
    Subtract two quantities.

    """
    q1 = Quantity(4.0, "cm * s**-1")
    q2 = Quantity(1.0, "cm * s**-1")
    q3 = Quantity(3.0, "cm * s**-1")
    q4 = Quantity(1.0, "cm")

    assert q1 - q2 == q3
    #assert Exception q1 - q4

def test_multiplication():
    """
    Multiply two quantities.

    """
    q1 = Quantity(2.0, "g * cm**2 * s**-3 * K")
    q2 = Quantity(3.0, "g * cm**-2 * s**-1 * K")
    q3 = Quantity(6.0, "g**2 * s**-4 * K**2")

    assert q1 * q2 == q3

def test_multiplication_with_number():
    """
    Multiply a quantity by a float.

    """
    u1 = Unit("g * cm / s")
    q1 = Quantity(2, u1)
    number = 3

    q2 = q1 * number

    assert q2.data == 6
    assert q2.units == u1

def test_division():
    """
    Divide two quantities.

    """
    q1 = Quantity(1.0, "g * cm**2 * s**-3 * K")
    q2 = Quantity(2.0, "g * cm**-2 * s**-1 * K")
    q3 = Quantity(0.5, "cm**4 * s**-2")

    assert q1 / q2 == q3

def test_equality():
    """
    Check equality conditions.

    """
    # @todo: more rigorous case
    q1 = Quantity(31536000, "s")
    q2 = Quantity(1.0, "yr")

    assert q1 == q2
