# -*- coding: utf-8 -*-
from invenio.utils import NATIONS_DEFAULT_MAP


def find_nations(field, subfields):
    result = []
    for x in field:
        if x[0] in subfields:
            for delimiter in [',', ' ']:
                values = [y.replace('.', '').lower().strip() for y in x[1].split(delimiter)]
                possible_affs = filter(lambda y: y is not None,
                                       map(dict((key.lower(), val) for (key, val) in NATIONS_DEFAULT_MAP.iteritems()).get, values))
                if possible_affs:
                    break
            if not possible_affs:
                possible_affs = ['HUMAN CHECK']
            if 'CERN' in possible_affs and 'Switzerland' in possible_affs:
                # Don't use remove in case of multiple Switzerlands
                possible_affs = [x for x in possible_affs
                                 if x != 'Switzerland']

            result.extend(possible_affs)

    result = sorted(list(set(result)))

    return result


def check_records(records, empty=False):
    fields = ['100', '700']

    for record in records:
        for field in fields:
            if field in record:
                for position, value in record.iterfield(field + '__w'):
                    record.delete_field(position)
                for i, x in enumerate(record[field]):
                    for val in find_nations(x[0], ['u', 'v']):
                        record.add_subfield((field + '__w', i, 0), 'w', val)
