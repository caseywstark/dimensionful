"""

Test unit functionality.

Copyright 2012, Casey W. Stark.

"""

import nose
import numpy as np

from utils import equal_sigfigs

from dimensionful.units import Unit, num_base

# @todo: global option?
required_precision = 4

def test_no_conflicting_symbols():
    """
    Construct full symbol list, check for conflicts.

    """
    from dimensionful.common_units import unit_symbols_dict, unit_prefixes
    full_set = set(unit_symbols_dict.keys())

    # go through all possible prefix combos
    for symbol in unit_symbols_dict.keys():
        for prefix in unit_prefixes.keys():
            new_symbol = "%s%s" % (prefix, symbol)

            # test if we have seen this symbol
            if new_symbol in full_set:
                print "Duplicate symbol: %s" % new_symbol
                return False

            full_set.add(new_symbol)

def test_dimensionless():
    """
    Create dimensionless unit. Check that dimensions are all zero and string
    representation is "(dimensionless)".

    """
    u1 = Unit()
    assert ( (u1.dimensions == np.zeros(num_base)).all()
             and u1.conversion_factor == 1.0
             and u1.base_string == "(dimensionless)" )

def test_creation_from_symbols():
    """
    Create unit from string.

    """
    from dimensionful.common_units import energy

    u1 = Unit("g cm^2 s^-2")
    assert (u1.dimensions == energy).all() and u1.conversion_factor == 1.0

    u2 = Unit("cm^2 s^-2 g")  # different order
    assert (u2.dimensions == energy).all() and u2.conversion_factor == 1.0

def test_creation_from_powers():
    """
    Create unit using array of powers syntax.

    """
    from dimensionful.common_units import energy

    u1 = Unit((1, 2, -2, 0))
    assert (u1.dimensions == energy).all() and u1.conversion_factor == 1.0

    cf = 42
    u2 = Unit((1, 2, -2, 0), conversion_factor=cf)
    assert (u2.dimensions == energy).all() and u2.conversion_factor == cf

def test_creation_duplicate_dims():
    """
    Create unit with multiple symbols of the same dimension.

    """
    from dimensionful.common_units import power, rate

    u1 = Unit("erg s^-1")
    u2 = Unit("km s^-1 Mpc^-1")
    km_cgs = 1e5
    Mpc_cgs = 3.08568025e24

    assert (u1.dimensions == power).all() and u1.conversion_factor == 1.0
    assert (u2.dimensions == rate).all()
    assert equal_sigfigs(u2.conversion_factor, km_cgs / Mpc_cgs,
                         required_precision)

def test_conversion_factor():
    """
    Check that conversion factors are generated and are accurate. This test is
    a duplicate in many ways now, but it can't hurt to keep it.

    """
    from dimensionful.common_units import mass_density

    Msun_cgs = 1.98892e33
    Mpc_cgs = 3.08568025e24
    u1 = Unit("Msun Mpc^-3")

    assert (u1.dimensions == mass_density).all()
    assert equal_sigfigs(u1.conversion_factor, Msun_cgs * Mpc_cgs**-3,
                         required_precision)

def test_string_representation():
    """
    Check how a unit casts to a string.

    """
    from dimensionful.common_units import length

    u1 = Unit("cm")
    u2 = Unit("pc")
    #u3 = Unit("")

    assert str(u1) == "cm"
    assert str(u2) == "pc"
    #assert str(u3) == "pc"

def test_multiplication():
    """
    Multiply two units.

    """
    from dimensionful.common_units import momentum

    Msun_cgs = 1.98892e33
    pc_cgs = 3.08568025e18
    u1 = Unit("Msun s^-1")
    u2 = Unit("pc")

    u3 = u1 * u2

    assert (u3.dimensions == momentum).all()
    assert equal_sigfigs(u3.conversion_factor, Msun_cgs * pc_cgs,
                         required_precision)

def test_division():
    """
    Divide two units.

    """
    from dimensionful.common_units import rate

    pc_cgs = 3.08568025e18
    km_cgs = 1e5
    u1 = Unit("pc")
    u2 = Unit("km s")

    u3 = u1 / u2

    assert (u3.dimensions == rate).all()
    assert equal_sigfigs(u3.conversion_factor, pc_cgs / km_cgs,
                         required_precision)

def test_pow():
    """
    Take units to some power.

    """
    pc_cgs = 3.08568025e18
    mK_cgs = 1e-3
    u1_powers = np.array((1, 2, -3, 4))
    u1 = Unit("g pc^2 s^-3 mK^4")

    u2 = u1**2

    print "%e" % u2.conversion_factor
    print "%e" % (pc_cgs**2 * mK_cgs**4)**2

    assert (u2.dimensions == u1_powers*2).all()
    assert equal_sigfigs(u2.conversion_factor, (pc_cgs**2 * mK_cgs**4)**2,
                         required_precision)

    u3 = u1**(-1./3)
    assert (u3.dimensions == -1. / 3 * u1_powers).all()
    assert equal_sigfigs(u3.conversion_factor, (pc_cgs**2 * mK_cgs**4)**(-1./3),
                         required_precision)

def test_equality():
    """
    Verify unit equality checks.

    """
    u1 = Unit("km s^-1")
    u2 = Unit("m ms^-1")

    assert u1 == u2
