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
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Hide old FFTs.
"""

from invenio.bibdocfile import BibRecDocs
from invenio.search_engine import perform_request_search
from invenio.bibtask import write_message


def bst_fix_elsevier_missing_file_formats():
    ids = perform_request_search(p="980:Elsevier", of='intbitset')
    for one_id in ids:
        bibrec = BibRecDocs(one_id)
        bibtextdoc = bibrec.list_bibdocs()[0]
        latest_rev_number = bibtextdoc.get_latest_version()
        latest_rev_file_types = []

        for f in bibtextdoc.list_latest_files():
            if f.format not in latest_rev_file_types:
                latest_rev_file_types.append(f.format)

        tmp_rev = latest_rev_number - 1
        while tmp_rev >= 1:
            for f in bibtextdoc.list_version_files(tmp_rev):
                if f.format not in latest_rev_file_types:
                    bibtextdoc.add_file_new_format(f.fullpath,
                                                   docformat=f.format)
                    write_message("Add format %s from %s revision to the newest revision of record: %s" % (f.format, tmp_rev, one_id))
                    latest_rev_file_types.append(f.format)
            tmp_rev -= 1
