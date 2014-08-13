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

from invenio.NonComplianceCheck import NonComplianceChecks
from invenio.utils import amend_fields, add_fields
from invenio.config import CFG_PYLIBDIR
from os.path import join


def check_records(records, empty=False):
    path = join(CFG_PYLIBDIR,
                '/invenio/bibcheck_plugins/compliance_check_configs/')
    checks = NonComplianceChecks(compliance_names=['CC', 'Authors', 'SCOAP3'],
                                 files_path=path)

    for record in records:
        dic = checks.check(record)
        if '591' in record:
            amend_fields(record, '591__a', dic, 'Checking compliance')
        else:
            add_fields(record, '591__a', 'a', dic)
