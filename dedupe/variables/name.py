from __future__ import print_function

from parseratorvariable import ParseratorType, compareFields, comparePermutable
import probablepeople

PERSON = (('marital prefix',      ('PrefixMarital',)),
          ('given name',          ('GivenName',
                                   'FirstInitial')),
          ('middle name',         ('MiddleName',
                                   'MiddleInitial')),
          ('surname',             ('Surname',
                                   'LastInitial')),
          ('generational suffix', ('SuffixGenerational',)),
          ('other prefix',        ('PrefixOther',)),
          ('other suffix',        ('SuffixOther',)),
          ('nick name',           ('NickName',)))

HOUSEHOLD_A = (('marital prefix A',      ('PrefixMarital')),
               ('given name A',          ('GivenName',
                                          'FirstInitial')),
               ('middle name A',         ('MiddleName',
                                          'MiddleInitial')),
               ('surname A',             ('Surname',
                                          'LastInitial')),
               ('generational suffix A', ('SuffixGenerational',)),
               ('other prefix A',        ('PrefixOther',)),
               ('other suffix A',        ('SuffixOther',)),
               ('nick name A',           ('NickName',)))

HOUSEHOLD_B = (('marital prefix B',      ('SecondPrefixMarital',)),
               ('given name B',          ('SecondGivenName',
                                          'SecondFirstInitial')),
               ('middle name B',         ('SecondMiddleName',
                                          'SecondMiddleInitial')),
               ('surname B',             ('SecondSurname',
                                          'SecondLastInitial')),
               ('generational suffix B', ('SecondSuffixGenerational',)),
               ('other prefix B',        ('SecondPrefixOther',)),
               ('other suffix B',        ('SecondSuffixOther',)),
               ('nick name B',           ('SecondNickName',)))

CORPORATION = (('corporation name',         ('CorporationName',)),
               ('corporation org',          ('CorporationNameOrganization',)),
               ('corporation type',         ('CorporationLegalType',)),
               ('short form',               ('ShortForm',)),
               ('client corporation name',  ('CorporationName',)),
               ('client corporation org',   ('CorporationNameOrganization',)),
               ('client corporation type',  ('CorporationLegalType',)),
               ('client short form',        ('ShortForm',)))


AKA_CORPORATION = (('other corporation name',  ('CorporationName',)),
                   ('other corporation org',   ('CorporationNameOrganization',)),
                   ('other corporation type',  ('CorporationLegalType',)),
                   ('other short form',        ('ShortForm',)))


class WesternNameType(ParseratorType) :
    type = "Name"

    def tagger(self, field) :
        return probablepeople.tag(field)

    components = (('Person' , compareFields, PERSON),
                  ('Corporation', compareFields, CORPORATION),
                  ('Household', comparePermutable, HOUSEHOLD_A,
                   HOUSEHOLD_B))


        
