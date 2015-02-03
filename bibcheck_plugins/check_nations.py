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


def find_nations(field, subfields):
    result = []
    for x in field:
        if x[0] in subfields:
            for delimiter in [',', ' ']:
                values = [y.replace('.', '').lower().strip() for y in x[1].replace('\n', ' ').split(delimiter)]
                possible_affs = filter(lambda y: y is not None,
                                       map(dict((key.lower(), val) for (key, val) in NATIONS_DEFAULT_MAP.iteritems()).get, values))
                if possible_affs:
                    break
            if not possible_affs:
                possible_affs = []
                for country in NATIONS_DEFAULT_MAP.itervalues():
                    if country.lower() in x[1].lower().replace('\n', ' '):
                        possible_affs.append(country)
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
            if field in record:
                for i, x in enumerate(record[field]):
                    new_countries = find_nations(x[0], ['u', 'v'])
                    current_countries = get_current_countries(x[0])

                    if new_countries is not current_countries:
                        ## FIXME
                        for key, val in enumerate(x[0]):
                            if "w" in val:
                                del x[0][key]
                                record.set_amended('Adding new countries')
                        # for position, value in record.iterfield(field + '__w'):
                        #     record.delete_field(position)
                        for val in new_countries:
                            record.add_subfield((field + '__w', i, 0), 'w', val)
