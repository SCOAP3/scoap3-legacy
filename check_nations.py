# -*- coding: utf-8 -*-
from invenio.utils import NATIONS_DEFAULT_MAP


def find_nations(field, subfields):
    result = []
    for x in field:
        if x[0] in subfields:
            values = [x.replace('.', '') for x in x[1].split(', ')]
            possible_affs = filter(lambda x: x is not None,
                                   map(NATIONS_DEFAULT_MAP.get, values))
            if len(possible_affs) == 1:
                result.append(possible_affs[0])
            else:
                result.append('HUMAN CHECK')

    if len(result) == 1:
        return result[0]
    else:
        return 'HUMAN CHECK'


def has_field(field, subfield):
    for x in field:
        if x[0] == subfield:
            return True
    return False


def check_records(records, empty=False):
    fields = ['100', '700']

    for record in records:
        for field in fields:
            if field in record:
                for i, x in enumerate(record[field]):
                    data = x[0]
                    if not has_field(data, 'w'):
                        val = find_nations(data, ['u', 'v'])
                        record.add_subfield((field + '__w', i, 0), 'w', val)
