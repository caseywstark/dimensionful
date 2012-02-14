"""

Basic testing utils. Because unittest is too complicated.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

"""

def equal_sigfigs(data1, data2, sig_figs):
    """
    Tests if the numbers given are equal up to some number of significant
    figures.

    The popular Python testing frameworks only have functions to assert that two
    numbers are equal up to some absolute decimal place. This is useless for
    very small numbers. This function tests for the precision of the two numbers
    instead.

    """
    average = (data1 + data2) / 2
    return round( (data1 - data2) / average, sig_figs) == 0.0

