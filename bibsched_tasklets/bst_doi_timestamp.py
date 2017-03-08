# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2014, 2017 CERN.
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
BibTasklet to discover new DOIs as they come by.
"""

import re
from datetime import datetime, timedelta

from invenio.bibtask import task_update_progress, write_message
from invenio.crossrefutils import get_all_modified_dois
from invenio.dbquery import run_sql
from urllib2 import URLError
import socket


CFG_SCOAP3_DOIS = {
    "10.1016": re.compile(r"^%s|^%s" % (re.escape("10.1016/j.physletb."), re.escape("10.1016/j.nuclphysb.")), re.I),  # Elsevier
    "10.1155": None,  # Hindawi
    "10.1088": re.compile(r"^10\.1088\/(1674-1137|1475-7516|1367-2630)", re.I),  # IOPP,
    "10.5506": re.compile(r"^10\.5506\/APhysPolB\.", re.I),  # Acta
    "10.1093": re.compile(r"^10\.1093\/ptep\/", re.I),  # Oxford
    "10.1140": re.compile(r"^10\.1140\/epjc\/", re.I),  # Springer EPJC
    "10.1007": re.compile(r"^10\.1007\/JHEP", re.I)  # Springer Sissa
}


def prepate_doi_table():
    run_sql("""CREATE TABLE IF NOT EXISTS doi (
        doi varchar(255) NOT NULL,
        creation_date datetime NOT NULL,
        publication_date datetime DEFAULT NULL,
        PRIMARY KEY doi(doi),
        KEY (creation_date)
    ) ENGINE=MyISAM;""")


def bst_doi_timestamp(reset=0):
    prepate_doi_table()
    now = datetime.now()
    last_run = ((run_sql("SELECT max(creation_date) FROM doi")[0][0] or datetime(2014, 1, 1)) - timedelta(days=4)).strftime("%Y-%m-%d")
    if int(reset):
        last_run = (datetime(2014, 1, 1) - timedelta(days=4)).strftime("%Y-%m-%d")
    write_message("Retrieving DOIs modified since %s" % last_run)
    restart_on_error = True
    while restart_on_error:
        restart_on_error = False
        for publisher, re_match in CFG_SCOAP3_DOIS.items():
            task_update_progress("Retrieving DOIs for %s" % publisher)
            write_message("Retriving DOIs for %s" % publisher)
            try:
                res = get_all_modified_dois(publisher, last_run, re_match, debug=True)
                for doi in res:
                    if publisher == "10.1093":
                        db_entry = run_sql("SELECT doi, publication_date FROM doi WHERE doi=%s", (doi, ))
                        pub_date = None
                        if 'published-online' in res[doi]:
                            if len(res[doi]['published-online']['date-parts'][0]) == 3:
                                pub_date = datetime.strptime('-'.join(map(str,res[doi]['published-online']['date-parts'][0])),"%Y-%m-%d")

                        write_message(db_entry)
                        if db_entry:
                            if db_entry[0][1]:  # publication date is in the system
                                continue
                            else:
                                if pub_date:
                                    run_sql("UPDATE doi SET publication_date = %s WHERE doi=%s", (pub_date, doi))
                                else:
                                    continue
                        else:
                           write_message("New DOI discovered for publisher %s: %s, publication: %s" % (publisher, doi, pub_date))
                           if pub_date:
                                run_sql("INSERT INTO doi(doi, creation_date, publication_date) VALUES(%s, %s, %s)", (doi, now, pub_date))
                           else:
                                run_sql("INSERT INTO doi(doi, creation_date) VALUES(%s, %s)", (doi, now))
                    else:
                        if run_sql("SELECT doi FROM doi WHERE doi=%s", (doi, )):
                            continue
                        write_message("New DOI discovered for publisher %s: %s" % (publisher, doi))
                        run_sql("INSERT INTO doi(doi, creation_date) VALUES(%s, %s)", (doi, now))
            except URLError as e:
                write_message("%s %s %s" % (publisher, last_run, re_match))
                write_message("Problem with connection! %s" % (e,))
                #restart_on_error = True
            except socket.timeout as e:
                write_message("Timeout error %s" % (e,))
                write_message("Finishing and rescheduling")
                #restart_on_error = True
            except ValueError as e:
                write_message("Value error in JSON string! %s" % (e,))
                #restart_on_error = True

