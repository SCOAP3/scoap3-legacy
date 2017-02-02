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

from invenio.webpage import pageheaderonly, pagefooteronly
from invenio.access_control_admin import acc_is_user_in_role, acc_get_role_id
from invenio.webuser import collect_user_info, page_not_authorized
from invenio.dbquery import run_sql
from invenio.bibrecord import record_get_field_values
from invenio.search_engine import (perform_request_search,
                                   get_record)
import datetime
import json


def index(req):
    user_info = collect_user_info(req)
    if not acc_is_user_in_role(user_info, acc_get_role_id("SCOAP3")):
        return page_not_authorized(req=req)

    req.content_type = "text/html"
    req.write(pageheaderonly("Repository tools & extra resources", req=req))
    req.write("<h1>Repository tools</h1>")

    req.write("<h2>Compliance</h2>")
    req.write("<a href='/compliance.py'>Content compliance</a> - articles compliance with agreements<br />")
    req.write("<a href='/compliance.py/csv'>Content compliance to CSV</a> - articles compliance with agreements<br />")
    req.write("<a href='/nations.py/late'>24h deadline</a> - checks the 24h delivery deadline (OBSOLETE)<br />")

    req.write("<h2>National statistics</h2>")
    req.write("<a href='/nations.py'>Countries impact</a> - number of pulications per country<br />")
    req.write("<a href='/nations.py/us_affiliations'>US affiliations</a> - all US affiliations<br />")
    req.write("<a href='/nations.py/us_affiliations_csv'>Selected US aff count CSV</a> - affiliation count for selected US universities<br />")
    req.write("<a href='/nations.py/usa_papers'>Selected US articles list</a><br />")
    req.write("<a href='/nations.py/usa_papers_csv'>Selected US articles list CSV</a><br />")
    req.write("<a href='/nations.py/papers_by_country_csv?country=xxx'>CSV list of articles by country</a> - you need to change argument 'country=xxx' to a country from the list bellow<br />")
    req.write("<textarea>Algeria, Argentina, Armenia, Australia, Austria, Azerbaijan, Belarus, Belgium, Bangladesh, Brazil, Bulgaria, Canada, CERN, Chile, China, Colombia, Costa Rica, Cuba, Croatia, Cyprus, Czech Republic, Denmark, Egypt, Estonia, Finland, France, Georgia, Germany, Greece, Hong Kong, Hungary, Iceland, India, Indonesia, Iran, Ireland, Israel, Italy, Japan, South Korea, Lebanon, Lithuania, Luxembourg, Mexico, Montenegro, Morocco, Niger, Netherlands, New Zealand, Norway, Pakistan, Poland, Portugal, Romania, Republic of San Marino, Russia, Saudi Arabia, Serbia, Singapore, Slovakia, South Africa, Spain, Sweden, Switzerland, Taiwan, Thailand, Tunisia, Turkey, Ukraine, UK, USA, Uruguay, Uzbekistan, Venezuela, Vietnam, Yemen, Peru, Kuwait, Sri Lanka, Kazakhstan, Mongolia, United Arab Emirates, United Arab Emirates, Malaysia, Qatar, Kyrgyz Republic, Jordan</textarea>")
    req.write("<a href='https://repo.scoap3.org/nations.py/countries_by_publishers'>Countries per journals</a>")

    req.write("<h2>Articles for impact calculations</h2>")
    req.write("<a href='/nations.py/impact_articles?year=2014'>Countries impact for 2014</a><br />")
    req.write("<a href='https://gist.github.com/Dziolas/7924d2feb2b3e5b0618a'>Code to run on Inspire server to get articles for impact calculation</a><br />")

    req.write("<h2>Export to INSPIRE</h2>")
    req.write("<a href='/ffts_for_inspire.py'>Data export</a><br />")
    req.write("<a href='/ffts_for_inspire.py/csv'>Data export to CSV</a><br />")

    req.write("<h1>Hidden collections</h1>")
    req.write("<a href='/collection/Erratum'>Erratas</a><br />")
    req.write("<a href='/collection/Addendum'>Addendums</a><br />")
    req.write("<a href='/collection/Corrigendum'>Corrigendums</a><br />")
    req.write("<a href='/collection/Editorial'>Editorials</a><br />")
    req.write("<a href='/collection/older_than_2014'>Articles older than 2014</a><br />")
    req.flush()

    req.write(pagefooteronly(req=req))
    return ""


def show_restricted_records(req):
    user_info = collect_user_info(req)
    if not acc_is_user_in_role(user_info, acc_get_role_id("SCOAP3")):
        return page_not_authorized(req=req)

    all_ids = [id[0] for id in run_sql("Select id from bibrec")]
    visible_ids = perform_request_search()

    deleted_and_older_and_restricted = set(all_ids) - set(visible_ids)
    restricted_ids = []
    # restricted_ids_older = []
    for id in deleted_and_older_and_restricted:
        rec = get_record(id)
        collections = record_get_field_values(rec, "980","%","%","%")
        if "DELETED" not in collections:
            year = record_get_field_values(rec, "773","%","%","y")
            title = record_get_field_values(rec, "245","%","%","a")
            if title:
                title = title[0]
            else:
                title = "No title"
            if year:
                if int(year[0]) >= 2015:
                    restricted_ids.append((id, title))
                # else:
                #    restricted_ids_older.append(id)
            else:
                restricted_ids.append((id,title))

    print "Restricted ids"
    print restricted_ids

    req.content_type = "text/html"
    req.write(pageheaderonly("Repository tools", req=req))
    req.write("<h1>Restricted records</h1>")
    req.write("<strong>Total number of possibli restricted records: {0}</strong>".format(len(restricted_ids)))
    req.write("<ol>")
    for id, title in restricted_ids:
        req.write("<li><a href='http://repo.scoap3.org/record/{1}'>{0}</a> <a href='http://repo.scoap3.org/record/edit/?ln=en#state=edit&recid={1}'>edit</a></li>".format(title, id))
    req.write("</ol>")
    # for id, title in restricted_ids:
    #    req.write("{0},".format(id))

    req.write(pagefooteronly(req=req))
    return ""

def package_arrival(req, doi=None, package_name=None):
    req.content_type = "text/html"
    req.write(pageheaderonly("Repository tools - packages arrival", req=req))
    req.write("<h1>Packages Arrivals</h1>")
    req.write("""<form action='/tools.py/package_arrival' method='get'>
                       <label for='doi'>DOI: </label>
                       <input type='text' name='doi' value='{0}'>
                       <label for='package_name'>Package Name: </label>
                       <input type='text' name='package_name' value='{1}'>
                       <input type='submit'>
                     </form>""".format(doi, package_name))
    if doi:
        req.write("<h1>Results for doi: {0}</h1>".format(doi))
        req.write("""<table>
                       <thead>
                         <th>#</th>
                         <th>Package name</th>
                         <th>Date</th>
                       </thead>""")
        packages = run_sql("select package.name as name, package.delivery_date as date from doi_package join package on doi_package.package_id = package.id WHERE doi_package.doi=%s", (doi,))
        #req.write(str(packages))

    if package_name:
        req.write("<h1>Results for package: {0}</h1>".format(package_name))
        req.write("""<table>
                       <thead>
                         <th>#</th>
                         <th>Package name</th>
                         <th>Date</th>
                       </thead>""")
        packages = run_sql("select package.name as name, package.delivery_date as date from package WHERE package.name like '%{0}%'".format(package_name))
        #req.write(str(packages))

    if packages:
        for i, package in enumerate(packages):
           req.write("<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(i+1, package[0], package[1]))
        req.write("</table>")

    req.write(pagefooteronly(req=req))
    return ""


def get_collections_count(req, callback=''):
    a = {'journals': {'Acta':0,
                      'Advances in High Energy Physics':0,
                      'Chinese Physics C':0,
                      'European Physical Journal C':0,
                      'Journal of Cosmology and Astroparticle Physics':0,
                      'Journal of High Energy Physics':0,
                      'New Journal of Physics':0,
                      'Nuclear Physics B':0,
                      'Physics Letters B':0,
                      'Progress of Theoretical and Experimental Physics':0
                      },
         'other':{}
         }
    for key in a['journals']:
        a['journals'][key] = len(perform_request_search(c=key))
    a['other']['all'] = len(perform_request_search())
    a['other']['this_year'] = len(perform_request_search(p="year:%s" % (datetime.date.today().year,)))
    a['other']['yesterday'] = len(perform_request_search(p="datecreated:%s" % (datetime.date.today() - datetime.timedelta(days=1),)))
    return '%s(%s)' % (callback, json.dumps(a))
