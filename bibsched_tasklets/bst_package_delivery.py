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
BibTasklet to discover new DOIs as they come by.
"""

import re
import sys
from datetime import datetime, timedelta
from invenio.bibtask import write_message

from invenio.dbquery import run_sql
import traceback


def prepare_package_table():
    return run_sql("""CREATE TABLE IF NOT EXISTS package (
        id mediumint NOT NULL AUTO_INCREMENT,
        name varchar(255) NOT NULL UNIQUE,
        delivery_date datetime NOT NULL,
        PRIMARY KEY doi(id),
        KEY (name)
    ) ENGINE=MyISAM;""")


def prepare_doi_package_table():
    return run_sql("""CREATE TABLE IF NOT EXISTS doi_package (
        package_id mediumint NOT NULL,
        doi varchar(255) NOT NULL,
        PRIMARY KEY doi_pacakge(package_id, doi),
        FOREIGN KEY (package_id)
            REFERENCES package(id)
            ON DELETE CASCADE,
        FOREIGN KEY (doi)
            REFERENCES doi(doi)
            ON DELETE CASCADE
    ) ENGINE=MyISAM;""")


def bst_package_delivery(packages, doi_package):
    prepare_package_table()
    prepare_doi_package_table()

    packages_file = open(packages)
    doi_package_file = open(doi_package)

    package = packages_file.readlines()
    doi_package = doi_package_file.readlines()

    for p in package:
        delivery_date, name = p.strip().split()
        if run_sql("SELECT name FROM package WHERE name=%s", (name, )):
            continue
        else:
            print "New pacakge discovered for publisher %s: %s" % ('Elsevier', name)
            run_sql("INSERT INTO package(name, delivery_date) VALUES(%s, %s)", (name, delivery_date))

    for dp in doi_package:
        try:
            p_name, doi = dp.strip().split()
            p_id = run_sql("SELECT id FROM package WHERE name=%s", (p_name,))
            try:
                run_sql("INSERT INTO doi_package VALUES(%s, %s)", (p_id[0][0], doi))
            except Exception as e:
                write_message(e)
                write_message("This already exist: %d %s" % (p_id[0][0], doi))
        except:
            pass
