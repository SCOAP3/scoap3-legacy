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

from invenio.bibdocfile import BibRecDocs
from harvestingkit.jats_utils import JATSParser
from harvestingkit.nlm_utils import NLMParser
from harvestingkit.utils import add_nations_field
from xml.dom.minidom import parseString


def is_springer(record):
    fields = ['980', '260']
    for field in fields:
        if field in record:
            for values in record[field][0][0]:
                if 'Springer' in values or 'SISSA' in values:
                    return True
    return False


def check_records(records):
    for record in records:
        if is_springer(record):
            rec_doc = BibRecDocs(int(record.record_id))
            rec_docs = rec_doc.list_latest_files()
            for doc in rec_docs:
                if doc.get_format() == '.xml':
                    f = open(doc.get_full_path())
                    content = f.read()
                    try:
                        del record['100']
                        del record['700']
                        record.amended = True
                    except:
                        pass

                    first_author = True
                    try:
                        if "-//NLM//DTD JATS" in content:
                            jats = JATSParser()
                            authors = jats.get_authors(parseString(content))
                        else:
                            app = NLMParser()
                            authors = app.get_authors(parseString(content))
                    except:
                        record.warn('Problem with parsing XML.')
                        continue

                    for author in authors:
                        if author.get('surname'):
                            subfields = [('a', '%s, %s' % (author.get('surname'), author.get('given_name') or author.get('initials', '')))]
                        else:
                            subfields = [('a', '%s' % (author.get('name', '')))]
                        if 'orcid' in author:
                            subfields.append(('j', author['orcid']))
                        if 'affiliation' in author:
                            for aff in author["affiliation"]:
                                subfields.append(('v', aff))

                        add_nations_field(subfields)

                        if author.get('email'):
                                subfields.append(('m', author['email']))
                        if first_author:
                            record.add_field('100__', value='', subfields=subfields)
                            first_author = False
                        else:
                            record.add_field('700__', value='', subfields=subfields)
