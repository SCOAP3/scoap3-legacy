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

"""
Amend cc-by to CC-BY-3.0 or CC-BY-4.0
"""
from invenio.bibrecord import record_get_field_value

def check_records(records):
    """
    Amend cc-by to CC-BY-3.0 or CC-BY-4.0
    """
    for record in records:
        cc_by_url = record_get_field_value(record, '540', code='u')
        cc_by_30 = '3.0' in cc_by_url
        cc_by_40 = '4.0' in cc_by_url
        for position, value in record.iterfield('540__a'):
            if not value.startswith('CC-BY-'):
                if value.startswith('cc-by'):
                    if cc_by_30:
                        record.amend_field(position, 'CC-BY-3.0')
                    elif cc_by_40:
                        record.amend_field(position, 'CC-BY-4.0')
                    else:
                        record.amend_field(position, 'CC-BY')
                        record.warn("Unknown CC-BY revision: %s" % cc_by_url)
                else:
                    record.set_invalid("Unknown License: %s with url %s" % (value, cc_by_url))

