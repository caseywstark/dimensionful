"""

Parse strings of math into symbols.

Copyright 2012, Casey W. Stark.

"""

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
