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

    req.write("<h2>Export to INSPIRE</h2>")
    req.write("<a href='/ffts_for_inspire.py'>Data export</a><br />")
    req.write("<a href='/ffts_for_inspire.py/csv'>Data export to CSV</a><br />")
    req.flush()

    req.write(pagefooteronly(req=req))
    return ""
