from __future__ import print_function

import functools
from parseratorvariable import ParseratorType, comparePermutable, consolidate, compareString
import probablepeople
from .gender import gender_names
import numpy

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
          ('nick name',           ('NickName',)),
          ('gender',              ('Gender',)),
          ('has generational suffix', ('HasSuffixGenerational')))


FIRST_NAMES_A = (('marital prefix A',      ('PrefixMarital')),
                 ('given name A',          ('GivenName',
                                            'FirstInitial')),
                 ('middle name A',         ('MiddleName',
                                            'MiddleInitial')),
                 ('other prefix A',        ('PrefixOther',)),
                 ('nick name A',           ('NickName',)))

LAST_NAMES_A = (('surname A',             ('Surname',
                                          'LastInitial')),
                ('generational suffix A', ('SuffixGenerational',)),
                ('other suffix A',        ('SuffixOther',)))

FIRST_NAMES_B = (('marital prefix B',      ('SecondPrefixMarital',)),
                 ('given name B',          ('SecondGivenName',
                                            'SecondFirstInitial')),
                 ('middle name B',         ('SecondMiddleName',
                                            'SecondMiddleInitial')),
                 ('other prefix B',        ('SecondPrefixOther',)),
                 ('nick name B',           ('SecondNickName',)))

LAST_NAMES_B = (('surname B',             ('SecondSurname',
                                           'SecondLastInitial')),
                ('generational suffix B', ('SecondSuffixGenerational',)),
                ('other suffix B',        ('SecondSuffixOther',)))

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


_, FIRST_NAMES_A_PARTS = list(zip(*FIRST_NAMES_A))
_, FIRST_NAMES_B_PARTS = list(zip(*FIRST_NAMES_B))
_, LAST_NAMES_A_PARTS = list(zip(*LAST_NAMES_A))

COMBO_NAMES = len(FIRST_NAMES_A) + len(LAST_NAMES_A)

FIRST_NAME_PLACES = numpy.array([False] * (COMBO_NAMES * 2))
FIRST_NAME_PLACES[0:len(FIRST_NAMES_A)] = True
FIRST_NAME_PLACES[COMBO_NAMES:COMBO_NAMES+len(FIRST_NAMES_A)] = True

def compareHouseholds(tags_a, tags_b, field_1, field_2) :
    all_tags = set().union(field_1.keys(), field_2.keys())

    if {'SecondSurname', 'SecondLastInitial'} & all_tags :
        return comparePermutable(tags_a, tags_b, field_1, field_2)

    else :
        distances = numpy.empty(len(tags_a) * 2)
        distances[:] = numpy.nan

        first_name_dist = comparePermutable(FIRST_NAMES_A_PARTS,
                                            FIRST_NAMES_B_PARTS,
                                            field_1,
                                            field_2)
        distances[FIRST_NAME_PLACES] = first_name_dist

        last_name_dist = list(compareFields(LAST_NAMES_A_PARTS,
                                            field_1,
                                            field_2))
        distances[len(FIRST_NAMES_A) : COMBO_NAMES] = last_name_dist

        return distances

def compareFields(parts, field_1, field_2) :
    joinParts = functools.partial(consolidate, components=parts)   
    for part, (part_1, part_2) in zip(parts, zip(*map(joinParts, [field_1, field_2]))) :
        if part == ('Gender',) :
            yield part_1 + part_2 - 2 * part_1 * part_2
        elif part == ('HasSuffixGenerational',) :
            if bool(part_1) != bool(part_2) : # exclusive or
                yield 1.0
            else :
                yield 0.0
        else :
            yield compareString(part_1, part_2)



class WesternNameType(ParseratorType) :
    type = "Name"

    def tagger(self, field) :
        tags, name_type = probablepeople.tag(field)
        tags['Gender'] = gender_names.get(tags.get('GivenName', None), 
                                          numpy.nan)
        tags['HasSuffixGenerational1'] = tags.get('SuffixGenerational', None)
        tags['HasSuffixGenerational2'] = tags.get('SuffixGenerational', None)
        return tags, name_type


    components = (('Person' , compareFields, PERSON),
                  ('Corporation', compareFields, CORPORATION),
                  ('Household', compareHouseholds, 
                   FIRST_NAMES_A + LAST_NAMES_A,
                   FIRST_NAMES_B + LAST_NAMES_B))




        
