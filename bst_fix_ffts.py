## This file is part of SCOAP3.
## Copyright (C) 2014 CERN.
##
## SCOAP3 is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## SCOAP3 is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with SCOAP3; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from invenio.search_engine import perform_request_search
from invenio.bibdocfile import BibRecDocs, InvenioBibDocFileError
from invenio.bibdocfilecli import bibupload_ffts
from invenio.bibtask import write_message, task_sleep_now_if_required
from invenio.errorlib import register_exception

def get_broken_recids():
    return perform_request_search(p="filetype:xml and not filetype:pdf", of='intbitset')

def get_last_pdf_for_record(bibrecdocs):
    bibdoc = bibrecdocs.list_bibdocs()[0]
    all_versions = bibdoc.list_versions()
    all_versions.reverse()
    for version in all_versions:
        try:
            return bibdoc.get_file('.pdf', version=version)
        except InvenioBibDocFileError:
            ## This version does not have any PDF
            continue

def build_fft(bibdocfile):
    return {
        'a': bibdocfile.get_path(),
        'n': bibdocfile.get_name(),
        'f': bibdocfile.get_format(),
    }

def bst_fix_ffts(debug=0):
    debug = bool(int(debug))
    ffts = {}
    for recid in get_broken_recids():
        task_sleep_now_if_required(can_stop_too=True)
        write_message("Fixing %s" % recid)
        try:
            ffts[recid] = [build_fft(get_last_pdf_for_record(BibRecDocs(recid)))]
        except:
            register_exception(alert_admin=True)
    write_message("Uploading corrections")
    bibupload_ffts(ffts, append=True, do_debug=debug, interactive=False)
    return True

if __name__ == "__main__":
    bst_fix_ffts()
