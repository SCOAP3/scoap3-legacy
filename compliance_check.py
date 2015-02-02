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

from invenio.NonComplianceCheck import NonComplianceChecks
from invenio.config import CFG_PYLIBDIR
from os.path import join


def amend_fields(record, field, changes_dict, comment=''):
    """record : AmendableRecord"""
    for position, value in record.iterfield(field):
        key = value[:value.find(':')]
        if key in changes_dict:
            record.amend_field(position,
                               '%s:%d' % (key, changes_dict[key]),
                               comment)


def add_fields(record, field, subfield, value_dict, existing_values):
    """record : AmendableRecord"""
    ## FIXME
    for key, value in value_dict.iteritems():
        if key in [x[1].split(':')[0] for x in existing_values]:
            for position, val in existing_values:
                if key in val:
                    record.amend_field(position, '%s:%d' % (key, value))
                    break
        else:
            record.add_field(field,
                             value="",
                             subfields=[(subfield, '%s:%d' % (key, value))])


def check_records(records, empty=False):
    path = join(CFG_PYLIBDIR,
                'invenio/bibcheck_plugins/compliance_check_configs/')
    checks = NonComplianceChecks(compliance_names=['CC', 'Authors', 'SCOAP3'],
                                 files_path=path,
                                 regex_search_delimiter='//')

    for record in records:
        fields = []
        for position, value in record.iterfield('591__a'):
            fields.append((position, value))
        dic = checks.check(record)
        add_fields(record, '591__a', 'a', dic, fields)
