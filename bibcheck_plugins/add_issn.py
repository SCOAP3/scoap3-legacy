# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
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

from invenio.bibrecord import record_get_field_value

"""
Correct IOP ISSN into actual journal names
"""

CFG_ISSN_MAP = {
    'JCAP': '1475-7516',
    'New J. Phys.': '1367-2630',
    'Chinese Phys. C': '1674-1137',
    'Acta Physica Polonica B': '0587-4254',
    'Advances in High Energy Physics': '1687-7365',
    'EPJC': '1434-6052',
    'JHEP': '1029-8479',
    'Nuclear Physics B': '0550-3213',
    'Physics letters B': '0370-2693',
    'PTEP': '1347-4081'
}

def check_records(records, empty=False):
    """
    Adds ISSN to records.
    """
    for record in records:
        journal = record_get_field_value(record, '773', code='p')
        record.warn(journal)
        for journal_name in CFG_ISSN_MAP.iterkeys():
            if journal_name.lower() == journal.lower():
                if '022' in record:
                    if CFG_ISSN_MAP[journal_name] is not record_get_field_value(record, '022', code='a'):
                        for position, value in record.iterfield('022__a'):
                            record.amend_field(position, CFG_ISSN_MAP[journal_name])
                            record.warn("Amending")
                            break
                else:
                    record.add_field('022__', value='', subfields=[('a', CFG_ISSN_MAP[journal_name])])
                    record.warn("Adding")
