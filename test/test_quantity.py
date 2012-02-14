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
    Create a quantity object with a unit object as ``unit``
    parameter.

    """
    u1 = Unit("Mpc")
    q1 = Quantity(1.0, u1)

    assert q1.data == 1.0
    assert q1.units == u1

def test_creation_with_unit_string():
    """
    Create a quantity object with a unit symbol as ``unit``
    parameter.

    """
    u1 = Unit("Mpc")
    q1 = Quantity(1.0, "Mpc")

    assert q1.data == 1.0
    assert q1.units == u1

def test_string_representation():
    """
    Check how a quantity prints.

    """
    q1 = Quantity(1.0, "Mpc")

    assert str(q1) == "1.0 Mpc"

def test_conversion():
    """
    Convert a density quantity from CGS to cosmological units.

    """
    cosmological_density_units = Unit("Msun * Mpc**-3")
    q1 = Quantity(1e-29, "g * cm**-3")
    q1.convert_to("Msun * Mpc**-3")

    assert equal_sigfigs(q1.data, 1.47721e11, required_precision)
    assert q1.units == cosmological_density_units

def test_get_conversion():
    """
    Get a CGS density quantity in cosmological units.

    """
    cosmological_density_units = Unit("Msun * Mpc**-3")
    q1 = Quantity(1e-29, "g * cm**-3")
    q2 = q1.get_in("Msun * Mpc**-3")

    assert equal_sigfigs(q2.data, 1.47721e11, required_precision)
    assert q2.units == cosmological_density_units

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
