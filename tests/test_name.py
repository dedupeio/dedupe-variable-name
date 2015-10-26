import unittest
from dedupe.variables.name import WesternNameType

import numpy

class TestName(unittest.TestCase):

    def test_household(self) :
        name = WesternNameType({'field' : 'foo'})
        numpy.testing.assert_almost_equal(
            name.comparator('James and Rita Allen', 
                            'Rita and James Allen'),
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
             0, 0, 0, 0, 0.5, 0, 0, 0, 0.5, 
             0, 0, 0, 0.5, 0, 0, 0, 0, 0, 
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             1, 0, 0, 0, 1, 0, 0, 0, 1, 
             0, 0, 0, 0, 0, 0, 0])






def prettyPrint(variable, comparison) :
    for e in zip(variable.higher_vars, comparison) :
        print("%s:\t %s" % e)

