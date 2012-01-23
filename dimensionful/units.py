"""

Define units and operations.

Copyright 2012, Casey W. Stark.

"""

import copy
import string

import numpy as np

from dimensionful.common_units import unit_symbols_dict, unit_prefixes

### The "fundamental units"
# Here we define the base dimensions and their ordering.

# NB: For sanity, we use Gaussian E&M conventions. That is, charge is not
# a fundamental unit and you must use the appropriate form of E&M laws.

# these are constants so they should be uppercase, but I think that style is
# ugly, so please play nicely even though they are regularly named vars.
num_base = 4
base_dims = np.array(("mass", "length", "time", "temperature"))
cgs_dims = np.array(("g", "cm", "s", "K"))

dimensionless = np.array((0, 0, 0, 0))

def get_unit_from_symbol(symbol):
    """
    Parses a unit symbol for the dimensionality and conversion factor.

    Parameters
    ----------
    symbol : string
        The unit symbol. Expected syntax is unit symbols taken to powers with
        "^", separated by spaces. Examples are "cm^3" or "K g^-1".

    Returns
    -------
    unit : tuple
        Tuple of the powers array and the conversion factor. Syntax above.

    Examples
    --------
    >>> get_unit_from_symbol("K g^-1")
    (array([-1, 0, 0, 1]), 1)

    >>> get_unit_from_symbol("Msun Mpc^-3")
    (array([1, -3, 0, 0]), 6.769494e-41)

    """
    # @todo: allow other math syntax
    # @todo: use regex instead of stupid parsing

    dimensions = np.zeros(num_base)
    conversion_factor = 1.0

    symbol_string_split = symbol.split(" ")
    for symbol_element in symbol_string_split:
        # split the element into unit symbol and power
        element_split = symbol_element.split("^")
        element_symbol = element_split[0]
        element_power = 1
        if len(element_split) == 2:  # might not have a power
            element_power = float(element_split[1])

        # get the unit's dimensions and prefix if given
        unit_prefix = 1
        if unit_symbols_dict.has_key(element_symbol):
            symbol_tuple = unit_symbols_dict[element_symbol]
        else:
            possible_prefix = element_symbol[0]
            if unit_prefixes.has_key(possible_prefix):
                # the first character might be a prefix, check the rest of the
                # symbol
                symbol_wo_prefix = element_symbol[1:]

                if unit_symbols_dict.has_key(symbol_wo_prefix):
                    symbol_tuple = unit_symbols_dict[symbol_wo_prefix]
                    unit_prefix = unit_prefixes[possible_prefix]
                else:
                    raise Exception("Unknown symbol: %s." % element_symbol)
            else:
                raise Exception("Unknown symbol: %s." % element_symbol)

        element_dimensions = symbol_tuple[0]*element_power
        element_conversion = (unit_prefix * symbol_tuple[1])**element_power

        # @todo: make conversion a warning?
        #if symbol_tuple[1] != 1.0:
        #    print "Conversion: %s is %e" % (symbol_element, element_conversion)

        dimensions += element_dimensions
        conversion_factor *= element_conversion

    return (dimensions, conversion_factor)


class Unit:
    """
    Contains the dimensions and conversion factor for given unit. The default
    system is cgs, "God's units".

    """

    def __init__(self, unit_repr=None, conversion_factor=1.0):
        """
        Buid a unit with the given powers of the base units.

        Parameters
        ----------
        unit_repr : string or list-like
            Interprets the representation of the new units. The string form must
            be common unit symbols, separated by 1 space, with powers given by a
            caret, ^. A force would be "g cm s^-1". The list form must have the
            same number of elements as number of base units, giving the power of
            each base unit. A force would be (1, 1, -1, 0).
        conversion_factor : float
            The conversion factor to the default unit system, CGS.

        """
        # make dimensionless base to work with
        self.dimensions = np.zeros(num_base)
        self.conversion_factor = conversion_factor
        self.symbol_string = ""

        ### figure out how the unit is specified
        if isinstance(unit_repr, str):
            # base dimensions as ndarray
            # save symbol string
            self.symbol_string = unit_repr

            # parse it
            unit_tuple = get_unit_from_symbol(unit_repr)
            self.dimensions = unit_tuple[0]
            self.conversion_factor = unit_tuple[1]

        elif isinstance(unit_repr, np.ndarray):
            # base dimensions as ndarray
            if len(unit_repr) is not num_base:
                raise Exception("Wrong number of dimensions. There are %i base dimensions and you gave %i dimensions." % (num_base, len(unit_repr)))
            self.dimensions = unit_repr.copy()

        elif isinstance(unit_repr, tuple) or isinstance(unit_repr, list):
            # base dims as python stdlib data structure
            if len(unit_repr) is not num_base:
                raise Exception("Wrong number of dimensions. There are %i base dimensions and you gave %i dimensions." % (num_base, len(unit_repr)))
            for i in xrange(num_base):
                self.dimensions[i] = unit_repr[i]

        else:
            # Nothing passed, so assume the user wants it dimensionless. We
            # already have a dimensionless unit, so we don't need to do
            # anything.
            # @todo: maybe raise a warning...
            pass

        if not self.symbol_string:
            # unit was not constructed with a string, so just use cgs dimensions
            self.symbol_string = self.base_string

    @property
    def base_string(self):
        """ Get the string representation in terms of the cgs base units. """
        if not hasattr(self, "_base_string"):
            self._base_string = ""
            if not self.is_dimensionless():
                for symbol, power in zip(cgs_dims, self.dimensions):
                    if power == 0:
                        # this unit doesn't have any power of the current symbol
                        continue

                    if power == 1:
                        # no exponent if there is only 1
                        self._base_string += "%s " % symbol
                    else:
                        self._base_string += "%s^%i " % (symbol, power)

                # take off the extra space
                self._base_string = string.rstrip(self._base_string)
            else:
                self._base_string = "(dimensionless)"
        # done with memoization

        return self._base_string

    def __repr__(self):
        return self.symbol_string

    def __str__(self):
        return self.symbol_string

    def __mul__(self, other_unit):
        """ Multiply units (multiply conversions and add dimensions). """
        return Unit(self.dimensions + other_unit.dimensions,
                    self.conversion_factor * other_unit.conversion_factor)

    def __div__(self, other_unit):
        """ Divide units (divide conversions and subtract dimensions). """
        return Unit(self.dimensions - other_unit.dimensions,
                    self.conversion_factor / other_unit.conversion_factor)

    def __pow__(self, power):
        """
        Take units to some power (conversion to power, multiply dimensions).

        """
        return Unit(self.dimensions * power, self.conversion_factor**power)

    ### Comparison operators
    def same_dimensions_as(self, other_unit):
        """ Test if dimensions are the same. """
        return (self.dimensions == other_unit.dimensions).all()

    def __eq__(self, other_unit):
        """ Test equality of units. """
        if ( (self.dimensions == other_unit.dimensions).all()
             and self.conversion_factor == other_unit.conversion_factor ):
            return True
        return False

    def __gt__(self, other_unit):
        """ Test equality of units. """
        if ( (self.dimensions == other_unit.dimensions).all()
             and self.conversion_factor > other_unit.conversion_factor ):
            return True
        return False

    def __lt__(self, other_unit):
        """ Test equality of units. """
        if ( (self.dimensions == other_unit.dimensions).all()
             and self.conversion_factor < other_unit.conversion_factor):
            return True
        return False

    def is_dimensionless(self):
        """ Check if the units are dimensionless (all 0 powers). """
        return not self.dimensions.any()

    # @todo: finish lookup and data structure to check.
    def get_type(self):
        """
        Check dimensions against common dimensions defined, like energy or
        angular momentum. Return the string if we get a hit, otherwise
        "other".

        """
        if self.dimensions in common_dimensions:
            # get index
            pass
        return "other"
