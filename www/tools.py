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

from invenio.webinterface_handler_config import HTTP_BAD_REQUEST, SERVER_RETURN
from invenio.webpage import pagefooteronly, pageheaderonly, page
from invenio.config import CFG_SITE_URL
from os.path import join
from cgi import escape
from urllib import urlencode

from invenio.search_engine import (perform_request_search,
                                   get_creation_date,
                                   get_record)
from invenio.bibdocfile import BibRecDocs
from invenio.access_control_admin import acc_is_user_in_role, acc_get_role_id
from invenio.webuser import collect_user_info, page_not_authorized


def index(req):
    user_info = collect_user_info(req)
    if not acc_is_user_in_role(user_info, acc_get_role_id("SCOAP3")):
        return page_not_authorized(req=req)

    req.content_type = "text/html"
    req.write(pageheaderonly("Repository tools", req=req))
    req.write("<h1>Repository tools</h1>")

    req.write("<h2>Compliance</h2>")
    req.write("<a href='/compliance.py'>Content compliance</a> - articles compliance with agreements<br />")
    req.write("<a href='/compliance.py/csv'>Content compliance to CSV</a> - articles compliance with agreements<br />")
    req.write("<a href='/nations.py/late'>24h deadline</a> - checks the 24h delivery deadline<br />")

    req.write("<h2>National statistics</h2>")
    req.write("<a href='/nations.py'>Countries impact</a> - number of pulications per country<br />")
    req.write("<a href='/nations.py/us_affiliations'>US affiliations</a> - all US affiliations<br />")
    req.write("<a href='/nations.py/us_affiliations_csv'>Selected US aff count CSV</a> - affiliation count for selected US universities<br />")
    req.write("<a href='/nations.py/usa_papers'>Selected US articles list</a><br />")
    req.write("<a href='/nations.py/usa_papers_csv'>Selected US articles list CSV</a><br />")

    req.write("<h2>Export to INSPIRE</h2>")
    req.write("<a href='/ffts_for_inspire.py'>Data export</a><br />")
    req.write("<a href='/ffts_for_inspire.py/csv'>Data export to CSV</a><br />")
    req.flush()

    req.write(pagefooteronly(req=req))
    return ""
