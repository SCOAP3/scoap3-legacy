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

from invenio.bibrecord import record_get_field_value
from invenio.search_engine import get_creation_date
from invenio.bibtask import write_message


def check_records(records):
    for record in records:
        # adds missing data in year field
        year = record_get_field_value(record, '773', code='y')
        if not year:
            for position, value in record.iterfield('773__y'):
                record.amend_field(position, get_creation_date(record_get_field_value(record, '001'), '%Y'))

        # remove empty subfields
        if '773' in record:
            for subfield, value in record['773'][0][0]:
                if not value or value == '-':
                    for position, val in record.iterfield('773__%s' % (subfield,)):
                        record.delete_field(position, 'Deleteing empty field: %s' % (subfield,))
        else:
            write_message("Missing 773 field in record %s" % record_get_field_value(record, '001'))
