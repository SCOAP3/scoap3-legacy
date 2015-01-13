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

from invenio.search_engine import get_collection_reclist
from invenio.utils import flatten_list

journals = ['Acta',
            'Advances in High Energy Physics',
            'Chinese Physics C',
            'Journal of Cosmology and Astroparticle Physics',
            'New Journal of Physics']

rec_ids = map(str, flatten_list(map(get_collection_reclist, journals)))


def has_field(field, subfield):
    for x in field:
        if x[0] == subfield:
            return True
    return False


def check_records(records, empty=False):
    fields = ['100', '700']

    for record in records:
        if record.record_id in rec_ids:
            for field in fields:
                if field in record:
                    for i, x in enumerate(record[field]):
                        data = x[0]
                        if has_field(data, 'v'):
                            continue
                        for new_field in filter(lambda x: x[0] == 'u', data):
                            record.add_subfield((field + '__v', i, 0),
                                                'v', new_field[1])
                            data.remove(new_field)
