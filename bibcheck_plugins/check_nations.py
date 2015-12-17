# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2014, 2015 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from invenio.utils import NATIONS_DEFAULT_MAP
import re
from invenio.bibrecord import record_delete_subfield


def find_nations(field, subfields, record):
    result = []
    for x in field:
        if x[0] in subfields:
            possible_affs = []
            def _sublistExists(list1, list2):
                return ''.join(map(str, list2)) in ''.join(map(str, list1))
            values = set([y.lower().strip() for y in re.findall(ur"[\w']+", x[1].replace('.','').decode("UTF-8"), re.UNICODE)])
            record.warn(values)
            for key, val in NATIONS_DEFAULT_MAP.iteritems():
                key = unicode(key)
                key_parts = set(key.lower().decode('utf-8').split())
                if key_parts.issubset(values):
                    possible_affs.append(val)
                    values = values.difference(key_parts)
            record.warn("%s %s" % (possible_affs, x[1]))
            if not possible_affs:
                possible_affs = ['HUMAN CHECK']
            if 'CERN' in possible_affs and 'Switzerland' in possible_affs:
                # Don't use remove in case of multiple Switzerlands
                possible_affs = [x for x in possible_affs
                                 if x != 'Switzerland']

            result.extend(possible_affs)

    result = sorted(list(set(result)))

    return result


def get_current_countries(field):
    current_countries = []
    for f in field:
        if 'w' in f:
            for ff in f:
                if ff is not 'w':
                    current_countries.append(ff)
    return sorted(list(set(current_countries)))


def check_records(records, empty=False):
    fields = ['100', '700']

    for record in records:
        for field in fields:
            for pos, val in record.iterfield(field+"__w"):
                record.warn("%s %s" % (pos, val))
                record_delete_subfield(record, field, "w")
                record.set_amended('Removing old countries')
            if field in record:
                for i, x in enumerate(record[field]):
                    new_countries = find_nations(x[0], ['u', 'v'], record)
                    current_countries = get_current_countries(x[0])

                    if new_countries is not current_countries:
                        for val in set(new_countries):
                            record.add_subfield((field + '__w', i, 0), 'w', val)
