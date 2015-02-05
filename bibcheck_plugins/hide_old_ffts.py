# -*- coding: utf-8 -*-
##
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
Bibcheck pluginr for hiding old FFTs.
"""

from invenio.bibdocfile import BibRecDocs, CFG_BIBDOCFILE_AVAILABLE_FLAGS
from invenio.search_engine import perform_request_search
from invenio.bibtask import write_message


def get_record_id(record):
    position, value = record.iterfield('001___').next()
    return int(value)


def check_records(records):
    for record in records:
        one_id = get_record_id(record)
        bibrec = BibRecDocs(one_id)
        try:
            bibdoc = bibrec.list_bibdocs()[0]
            latest_rev = bibdoc.get_latest_version()

            i = 1
            while i < latest_rev:
                rev_file_types = []
                for f in bibdoc.list_version_files(i):
                    if f.format not in rev_file_types:
                        rev_file_types.append(f.format)
                for file_type in rev_file_types:
                    write_message("Record %s: hiding format %s in revision %s" % (one_id, file_type, i))
                    bibdoc.set_flag(CFG_BIBDOCFILE_AVAILABLE_FLAGS[3], file_type, i)
                i += 1
        except Exception as e:
            record.warn("Error when hiding previous files")
            record.warn(e)
