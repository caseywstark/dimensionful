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
    Create a Quantity with a Unit object as `unit` arg.

    """
    u1 = Unit("Mpc")
    q1 = Quantity(1.0, u1)

    assert q1.data == 1.0
    assert q1.units == u1

def test_creation_with_unit_string():
    """
    Create a Quantity with a unit symbol string as `unit` arg.

    """
    u1 = Unit("Mpc")
    q1 = Quantity(1.0, "Mpc")

    assert q1.data == 1.0
    assert q1.units == u1

def test_string_representation():
    """
    Check how a Quantity prints.

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
    else:
        assert False

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

def test_equality():
    """
    Test that Quantity equality checks work.

    """
    q1 = Quantity(1.0, "g * cm * s * K")
    q2 = Quantity(1.0, "g * cm * s * K")
    q3 = Quantity(1.0, "kg * cm * ms * K")
    q4 = Quantity(1.0 * 1e3, "g * cm * s * mK")

    assert q1 == q2
    assert q2 == q3
    assert q3 == q4

    # different type fail
    number = 1.0
    try:
        q1 == number
    except Exception:
        pass
    else:
        assert False

    # different dimensions fail
    q5 = Quantity(1.0, "g * cm * K")
    try:
        q1 == q5
    except Exception:
        pass
    else:
        assert False

def test_addition():
    """
    Add two quantities.

    """
    q1 = Quantity(1.0, "cm * s**-1")
    q2 = Quantity(2.0, "cm * s**-1")
    q3 = Quantity(3.0, "cm * s**-1")
    q4 = Quantity(1.0, "cm")
    q5 = Quantity(1.0, "km * hr**-1")
    q6 = Quantity(.01 + 1.e3 / 3600, "m * s**-1")
    q7 = Quantity(1.0, Unit())
    q8 = Quantity(2.0, Unit())
    number = 1.0

    # don't need to convert data to different units
    assert q3 == q1 + q2
    assert q3 == q2 + q1

    # test data conversion
    assert q6 == q1 + q5
    assert q6 == q5 + q1

    # float + dimensionless Quantity
    assert q8 == q7 + number
    assert q8 == number + q7

    # fail on different dimensions
    try:
        q1 + q4
    except Exception:
        pass
    else:
        assert False

    # fail on float + dimensionful Quantity
    try:
        q1 + number
    except Exception:
        pass
    else:
        assert False

def test_subtraction():
    """
    Subtract two quantities.

    """
    q1 = Quantity(3.0, "cm * s**-1")
    q2 = Quantity(1.0, "cm * s**-1")
    q3 = Quantity(2.0, "cm * s**-1")
    q4 = Quantity(1.0, "cm")
    q5 = Quantity(1.0, "km * hr**-1")
    q6 = Quantity(.01 - 1.e3 / 3600, "m * s**-1")
    q7 = Quantity(1.0, Unit())
    q8 = Quantity(2.0, Unit())
    number = 1.0

    # same units
    assert q3 == q1 - q2
    assert q3 == -q2 + q1

    # must convert data
    assert q6 == q2 - q5
    assert q6 == -q5 + q2

    # float + dimensionless Quantity
    assert q7 == q8 - number
    assert q7 == -number + q8

    # fail on different dimensions
    try:
        q1 - q4
    except Exception:
        pass
    else:
        assert False

    # fail on float + dimensionful Quantity
    try:
        q1 - number
    except Exception:
        pass
    else:
        assert False

def test_multiplication():
    """
    Multiply two quantities.

    """
    pc_cgs = 3.08568e18
    u1 = Unit("g * cm**2 * s**-3 * K")
    q1 = Quantity(2.0, "g * cm**2 * s**-3 * K")
    q2 = Quantity(3.0, "g * cm**-2 * s**-1 * K")
    q3 = Quantity(6.0, "g**2 * s**-4 * K**2")
    q4 = Quantity(5.0, "pc / cm / K")
    q5 = Quantity(2.0 * 5.0, "g * pc * cm * s**(-3)")
    q6 = Quantity(2.0 * 5.0 * pc_cgs, "g * cm**2 * s**-3")
    number = 3.0

    assert q3 == q1 * q2
    assert q3 == q2 * q1

    assert q5 == q1 * q4
    assert q5 == q4 * q1
    assert q6 == q1 * q4
    assert q6 == q4 * q1

    q7 = number * q1
    q8 = q1 * number

    assert q7.data == 2 * 3
    assert q8.data == 2 * 3
    assert q7.units == u1
    assert q8.units == u1

def test_division():
    """
    Divide two quantities.

    """
    pc_cgs = 3.08568e18
    u1 = Unit("g * cm**2 * s**-3 * K")
    q1 = Quantity(2.0, "g * cm**2 * s**-3 * K")
    q2 = Quantity(3.0, "g * cm**-2 * s**-1 * K")
    q3 = Quantity(2.0 / 3.0, "cm**4 * s**-2")
    q4 = Quantity(5.0, "pc / cm * K")
    q5 = Quantity(2.0 / 5.0, "g * cm**3 / pc * s**(-3)")
    q6 = Quantity(2.0 / 5.0 / pc_cgs, "g * cm**2 * s**-3")
    number = 3.0

    assert q3 == q1 / q2

    assert q5 == q1 / q4
    assert q6 == q1 / q4

    q7 = number / q1
    q8 = q1 / number

    assert q7.data == 3.0 / 2.0
    assert q8.data == 2.0 / 3.0
    assert q7.units == u1**-1
    assert q8.units == u1
