"""

Test unit functionality.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

"""

import nose

from utils import equal_sigfigs

from dimensionful.units import Unit

# @todo: global option?
required_precision = 4

def test_no_conflicting_symbols():
    """
    Construct full symbol list, check for conflicts.

    """
    from dimensionful.units import unit_symbols_dict, unit_prefixes
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
    Create dimensionless unit.
    Check that it thinks it is dimensionless with `is_dimensionless`.
    Verify by checking dimensions attribute.

    """
    u1 = Unit()
    assert u1.is_dimensionless and u1.dimensions == 1

def test_creation_from_symbol_string():
    """
    Create units from strings.

    """
    from dimensionful.dimensions import energy

    u1 = Unit("g * cm**2 * s**-2")
    assert u1.dimensions == energy and u1.cgs_value == 1.0

    u2 = Unit("cm**2 * s**-2 * g")  # different order
    assert u2.dimensions == energy and u2.cgs_value == 1.0

def test_creation_duplicate_dims():
    """
    Create unit with multiple symbols of the same dimension.

    """
    from dimensionful.dimensions import power, rate

    u1 = Unit("erg * s**-1")
    u2 = Unit("km * s**-1 * Mpc**-1")
    km_cgs = 1e5
    Mpc_cgs = 3.08568025e24

    assert u1.dimensions == power and u1.cgs_value == 1.0
    assert u2.dimensions == rate
    assert equal_sigfigs(u2.cgs_value, km_cgs / Mpc_cgs, required_precision)

def test_string_representation():
    """
    Check how a unit casts to a string.

    """
    from dimensionful.dimensions import length

    pc = Unit("pc")
    Myr = Unit("Myr")
    speed = pc / Myr

    assert str(pc) == "pc"
    assert str(Myr) == "Myr"
    assert str(speed) == "pc/Myr"

def test_multiplication():
    """
    Multiply two units.

    """
    from dimensionful.dimensions import momentum

    Msun_cgs = 1.98892e33
    pc_cgs = 3.08568025e18
    u1 = Unit("Msun * s**-1")
    u2 = Unit("pc")

    u3 = u1 * u2

    assert u3.dimensions == momentum
    assert equal_sigfigs(u3.cgs_value, Msun_cgs * pc_cgs, required_precision)

def test_division():
    """
    Divide two units.

    """
    from dimensionful.dimensions import rate

    pc_cgs = 3.08568025e18
    km_cgs = 1e5
    u1 = Unit("pc")
    u2 = Unit("km * s")

    u3 = u1 / u2

    assert u3.dimensions == rate
    assert equal_sigfigs(u3.cgs_value, pc_cgs / km_cgs, required_precision)

def test_pow():
    """
    Take units to some power.

    """
    from dimensionful.dimensions import mass, length, time, temperature

    pc_cgs = 3.08568025e18
    mK_cgs = 1e-3
    u1_dims = mass * length**2 * time**-3 * temperature**4
    u1 = Unit("g * pc**2 * s**-3 * mK**4")

    u2 = u1**2

    assert u2.dimensions == u1_dims**2
    assert equal_sigfigs(u2.cgs_value, (pc_cgs**2 * mK_cgs**4)**2,
                         required_precision)

    u3 = u1**(-1./3)
    assert u3.dimensions == u1_dims**(-1./3)
    assert equal_sigfigs(u3.cgs_value, (pc_cgs**2 * mK_cgs**4)**(-1./3),
                         required_precision)

def test_equality():
    """
    Verify unit equality checks.

    """
    u1 = Unit("km * s**-1")
    u2 = Unit("m * ms**-1")

    assert u1 == u2
