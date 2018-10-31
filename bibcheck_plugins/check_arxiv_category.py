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

import urllib

from xml.dom.minidom import parseString
from invenio.utils import get_doi
from invenio.bibrecord import create_record


def _query_arxiv_with_id(id):
    url = 'http://export.arxiv.org/api/query?search_query=id:{0}'
    try:
        data = urllib.urlopen(url.format(id)).read()
    except:
        data = None
    return data


def _get_arxiv_category(id):
    result = []
    data = _query_arxiv_with_id(id)

    if data:
        xml = parseString(data)
        for tag in xml.getElementsByTagName('arxiv:primary_category'):
            try:
                result.append(tag.attributes['term'].value)
            except KeyError:
                pass
        for tag in xml.getElementsByTagName('category'):
            try:
                result.append(tag.attributes['term'].value)
            except KeyError:
                pass
        return result
    else:
        return None


def _get_arxiv_id_from_record(record):
    for val in record['037'][0][0]:
        if 'arXiv:' in val[1]:
            return val[1].replace('arXiv:', '')
    raise Exception('Could not find an arXiv id.')


def _find_arxiv_id(inspire_rec):
    for field in inspire_rec['037']:
        data = field[0]
        for subfield in data:
            if 'a' == subfield[0] and 'arXiv:' in subfield[1]:
                return subfield[1].replace('arXiv:', '')
    raise Exception('Could not find an arXiv id')


def _add_arxiv_to_record(record, arxiv_id):
    record.add_subfield(('037__a', 0, 0), 'a', 'arXiv:'+arxiv_id)


def _get_arxiv_id_from_inspire(record):
    url = 'https://inspirehep.net/search?p=doi:{0}&of=xm'
    data = urllib.urlopen(url.format(get_doi(int(record.record_id)))).read()
    inspire_rec = create_record(data)[0]
    return _find_arxiv_id(inspire_rec)


def _get_arxiv_id(record):
    try:
        return _get_arxiv_id_from_record(record)
    except Exception:
        try:
            arxiv_id = _get_arxiv_id_from_inspire(record)
            _add_arxiv_to_record(record, arxiv_id)
            return arxiv_id
        except Exception:
            return ''


def _get_category_position(record):
    for position, val in record.iterfield('591__a'):
        if 'Category:' in val:
            return position


def _has_category_field(record):
    return any(filter(lambda x: 'Category'
               in x[1], record.iterfield('591__a')))


def check_records(records, empty=False):
    string = 'Category:{0}'

    for record in records:
        arxiv_id = _get_arxiv_id(record)

        if arxiv_id:
            categories = _get_arxiv_category(arxiv_id)
            sleep(2)
            if categories:
                if 'hep' in categories[0]:
                    string = 'Category:1'
                else:
                    string = 'Category:0'
                #val = string.format(int(any(filter(lambda x: 'hep' in x,
                #                                   categories))))
                if _has_category_field(record):
                    position = _get_category_position(record)
                    record.amend_field(position, val, '')
                else:
                    record.add_field('591__a', value='', subfields=[('a', val)])
            else:
                record.warn("Problem checking arXiv category.")
