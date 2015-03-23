from __future__ import print_function

from dedupe.variables.base import DerivedType
from dedupe.variables.string import StringType
import collections
import functools
import numpy
import probablepeople
from affinegap import normalizedAffineGapDistance as compareString

PERSON = (('marital prefix',      ('PrefixMarital')),
          ('given name',          ('GivenName',
                                   'FirstInitial')),
          ('middle name',         ('MiddleName',
                                   'MiddleInitial')),
          ('surname',             ('Surname',
                                   'LastInitial')),
          ('generational suffix', ('SuffixGenerational')),
          ('other prefix',        ('PrefixOther')),
          ('other suffix',        ('SuffixOther')),
          ('nick name',           ('NickName')))

HOUSEHOLD_A = (('marital prefix A',      ('PrefixMarital')),
               ('given name A',          ('GivenName',
                                          'FirstInitial')),
               ('middle name A',         ('MiddleName',
                                          'MiddleInitial')),
               ('surname A',             ('Surname',
                                          'LastInitial')),
               ('generational suffix A', ('SuffixGenerational')),
               ('other prefix A',        ('PrefixOther')),
               ('other suffix A',        ('SuffixOther')),
               ('nick name A',           ('NickName')))

HOUSEHOLD_B = (('marital prefix B',      ('SecondPrefixMarital')),
               ('given name B',          ('SecondGivenName',
                                          'SecondFirstInitial')),
               ('middle name B',         ('SecondMiddleName',
                                          'SecondMiddleInitial')),
               ('surname B',             ('SecondSurname',
                                          'SecondLastInitial')),
               ('generational suffix B', ('SecondSuffixGenerational')),
               ('other prefix B',        ('SecondPrefixOther')),
               ('other suffix B',        ('SecondSuffixOther')),
               ('nick name B',           ('SecondNickName')))

CORPORATION = (('corporation name',  ('CorporationName')),
               ('corporation name',  ('CorporationNameOrganization')),
               ('corporation type',  ('CorporationLegalType')),
               ('short form',        ('ShortForm')))
            
PERSON_NAMES, PERSON_PARTS = list(zip(*PERSON))
HOUSEHOLD_A_NAMES, HOUSEHOLD_A_PARTS = list(zip(*HOUSEHOLD_A))
HOUSEHOLD_B_NAMES, HOUSEHOLD_B_PARTS = list(zip(*HOUSEHOLD_B))
CORPORATION_NAMES, CORPORATION_PARTS = list(zip(*CORPORATION))

NameType = collections.namedtuple('NameType', 
                                  ['compare', 'indicator', 
                                   'offset'])

def consolidate(d, components) :
    for component in components :
        merged_component = ' '.join(d[part]  
                                    for part in component
                                    if part in d)
        yield merged_component

def compareFields(field_1, field_2, parts) :
    joinParts = functools.partial(consolidate, components=parts)    
    for part_1, part_2 in zip(*map(joinParts, [field_1, field_2])) :
        yield compareString(part_1, part_2)

def comparePermutable(field_1, field_2, tags_1, tags_2) :

    section_1A = tuple(consolidate(field_1, tags_1))
    section_1B = tuple(consolidate(field_1, tags_2))
    whole_2 = tuple(consolidate(field_2, tags_1 + tags_2))

    distances = [[compareString(part_1, part_2)
                 for part_1, part_2 
                 in zip(section_1A + section_1B, whole_2)]]

    distances += [[compareString(part_1, part_2)
                   for part_1, part_2 
                   in zip(section_1B + section_1A, whole_2)]]

    return numpy.min([numpy.nansum(distance) for distance in distances])

class WesternNameType(StringType) :
    type = "Name"

    components = {'Person' :
                      NameType(compare=functools.partial(compareFields,
                                            parts = PERSON_PARTS),
                               indicator=[0, 0],
                               offset=0),
                  'Corporation' :
                      NameType(compare=functools.partial(compareFields,
                                            parts = CORPORATION),
                                  indicator=[1, 0],
                                  offset= len(PERSON)),
                  'Household' :
                      NameType(compare=functools.partial(comparePermutable,
                                            tags_1 = HOUSEHOLD_A_PARTS,
                                            tags_2 = HOUSEHOLD_B_PARTS),
                               indicator=[0, 1],
                               offset = len(PERSON 
                                            + CORPORATION))}

    name_types = (PERSON + CORPORATION + HOUSEHOLD_A + HOUSEHOLD_B)

    # missing? + same_type? + len(indicator) + ... + full_string
    expanded_size = 1 + 1 + 1 + 2 + 2 * len(name_types) + 1

    def __len__(self) :
        return self.expanded_size


    def __init__(self, definition) :
        super(WesternNameType, self).__init__(definition)

        preamble = [('%s: Not Missing' % definition['field'], 'Dummy'),
                    ('ambiguous', 'Dummy'),
                    ('same name type?', 'Dummy'),
                    ('corporation', 'Dummy'),
                    ('household', 'Dummy')]

        name_parts = [(part, 'String') 
                      for part in self.name_types]

        self.n_parts = len(name_parts)

        not_missing_name_parts = [('%s: Not Missing' % (part,), 'Not Missing') 
                                     for part, _ in name_parts]

        fields = preamble + name_parts + not_missing_name_parts
        fields.append(('full string', 'String'))
        
        self.higher_vars = [DerivedType({'name' : name,
                                         'type' : field_type})
                            for name, field_type in fields]

    def comparator(self, field_1, field_2) :
        distances = numpy.zeros(self.expanded_size)
        i = 0

        if not (field_1 and field_2) :
            return distances
        
        distances[i] = 1
        i += 1

        try :
            name_1, name_type_1 = probablepeople.tag(field_1) 
            name_2, name_type_2  = probablepeople.tag(field_2)
        except Exception as e :
            print(e)
            return distances

        if 'Ambiguous' in (name_type_1, name_type_2) :
            distances[i:3] = [1, 0]
            distances[-1] = compareString(field_1, field_2)
            return distances
        elif name_type_1 != name_type_2 :
            distances[i:3] = [0, 0]
            distances[-1] = compareString(field_1, field_2)
            return distances
        elif name_type_1 == name_type_2 : 
            distances[i:3] = [0, 1]

        i += 2

        name_type = self.components[name_type_1]

        distances[i:5] = name_type.indicator
        i += 2

        i += name_type.offset
        for j, dist in enumerate(name_type.compare(name_1, name_2), 
                                 i) :
            distances[j] = dist

        unobserved_parts = numpy.isnan(distances[i:j+1])
        distances[i:j+1][unobserved_parts] = 0
        unobserved_parts = (~unobserved_parts).astype(int)
        distances[(i + self.n_parts):(j + 1 + self.n_parts)] = unobserved_parts

        return distances


        
