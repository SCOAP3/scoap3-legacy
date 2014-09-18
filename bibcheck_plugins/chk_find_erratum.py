## This file is part of Invenio.
## Copyright (C) 2014 CERN.
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

"""
Finds paper which are erratum, addendum or edditorial and assigns them an extra
collection: ERRATUM, ADDENDUM ,EDITORIAL or CORRIGENDUM.
"""
from invenio.bibrecord import record_get_field_value


def check_records(records):
    collections = {'errat': 'ERRATUM',
                   'addend': 'ADDENDUM',
                   'editor': 'EDITORIAL',
                   'corrigen': 'CORRIGENDUM'}

    for record in records:
        title = record_get_field_value(record, '245', code='a').lower()
        for phrase in collections.iterkeys():
            if phrase in title:
                field = record_get_field_value(record, '980', code='c')
                if field:
                    if field in ['ERRATUM', 'ADDENDUM', 'EDITORIAL','CORRIGENDUM']:
                        for position, value in record.iterfield('980__c'):
                            record.amend_field(position, collections[phrase])
                            break
                    else:
                        for position, value in record.iterfield('980__%'):
                            record.add_subfield(position, 'c', collections[phrase])
                            break
                else:
                    for position, value in record.iterfield('980__%'):
                        record.add_subfield(position, 'c', collections[phrase])
                        break
