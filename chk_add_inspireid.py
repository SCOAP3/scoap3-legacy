# -*- coding: utf-8 -*-
##
## This file is part of SCOAP3 Repository.
## Copyright (C) 2013 CERN.
##
## SCOAP3 Repository is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## SCOAP3 Repository is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with SCOAP3 Repository; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Add INSPIRE ID
"""
from invenio.bibrecord import record_get_field_values, record_get_field_value
from invenio.dbquery import run_sql
from invenio.urlutils import create_url
from urllib import urlopen
from time import sleep

def _init_db():
    """
    We keep a map of which DOI points to which INSPIRE ID, so that
    when a record is replaced we can readd the INSPIRE ID without querying
    INSPIRE.
    If you need to correct a relation, the corresponding row must be deleted
    from this table.
    """
    run_sql("""CREATE TABLE IF NOT EXISTS doi2inspireid (
        doi varchar(255) NOT NULL,
        inspireid mediumint(8) unsigned NOT NULL,
        creation_date datetime NOT NULL,
        PRIMARY KEY doi(doi),
        UNIQUE KEY (inspireid)
    ) ENGINE=MyISAM;""")


def check_records(records):
    """
    Add INSPIRE ID if missing
    """
    _init_db()
    for record in records:
        if 'INSPIRE' in record_get_field_values(record, '035', code='9'):
            ## Has already the link. Good! Let's go on.
            continue
        doi = record_get_field_value(record, '024', ind1='7', code='a')
        arxiv = record_get_field_value(record, '037', code='a')
        query = 'doi:"%s"' % doi
        if arxiv:
            query += ' or %s' % arxiv
        inspireid = run_sql("SELECT inspireid FROM doi2inspireid WHERE doi=%s", (doi,))
        if inspireid:
            inspireid = inspireid[0][0]
        else:
            sleep(2)
            inspireid = [int(elem.strip()) for elem in urlopen(create_url("http://inspirehep.net/search", {'cc': 'HEP', 'of': 'id', 'p': query})).read().strip()[1:-1].split(',') if elem.strip()]
            if len(inspireid) == 1:
                inspireid = inspireid[0]
                run_sql("INSERT INTO doi2inspireid(doi, inspireid, creation_date) VALUES(%s, %s, NOW())", (doi, inspireid))
            else:
                record.warn("More than one inspire ID matches this record: %s" % inspireid)
                continue
        record.add_field('035__', value=None, subfields=[('a', str(inspireid)), ('9', "INSPIRE")])
