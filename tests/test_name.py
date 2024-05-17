import unittest
from dedupe.variables.name import WesternNameType

import numpy

class TestName(unittest.TestCase):

    def test_household(self) :
        name = WesternNameType({'field' : 'foo'})
        numpy.testing.assert_almost_equal(
            name.comparator('James and Rita Allen',
                            'Rita and James Allen'),
            [ 1, 0, 1, 1, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0,
              0.5, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 1, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0])

    def test_person_type(self):
        name = WesternNameType({'field' : 'foo', 'name type' : 'person'})
        print(name.comparator('James and Rita Allen',
                              'Rita and James Allen'))

        numpy.testing.assert_almost_equal(
            name.comparator('James and Rita Allen',
                            'Rita and James Allen'),
            [ 1,   0,   1,   1,   0,   0,   0,
              0,   0,   0,   0,   0,   0,   0,   0,
              0,   0,   0,   0,   0.5,  0,   0,
              0,   0.5,  0,   0,   0,   0.5,  0,   0,
              0,   0,   0,   0,   0,   0,   0,
              0,   0,   0,   0,   0,   0,   0,   0,
              0,   0,   0,   0,   1,   0,   0,
              0,   1,   0,   0,   0,   1,   0,   0,
              0,   0,   0,   0,   0 ])

        predicates_parts = (getattr(p, "part", None) for p in name.predicates)
        assert not any(p == 'CorporationName' for p in predicates_parts)


    def test_company_type(self):
        name = WesternNameType({'field' : 'foo', 'name type' : 'company'})
        print(name.comparator('James and Rita Allen',
                              'Rita and James Allen'))

        numpy.testing.assert_almost_equal(
            name.comparator('James and Rita Allen',
                            'Rita and James Allen'),
            [ 1,  0,  1,  3.15625, 0,  0,  0,  0,
              0,  0,  0,  0,  0,  0,  0,  1,  0,
              0,  0,  0,  0,  0,  0,  0,  0,  0,
              0,  0])
        predicates_parts = (getattr(p, "part", None) for p in name.predicates)
        assert not any(p == 'Surname' for p in predicates_parts)

                                           
        
def prettyPrint(variable, comparison) :
    for e in zip(variable.higher_vars, comparison) :
        print("%s:\t %s" % e)
                                           
                                           
