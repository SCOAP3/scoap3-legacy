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

import re

from os import listdir
from os.path import join
from xml.dom.minidom import parse
from harvestingkit.minidom_utils import xml_to_text
from invenio.utils import get_doc_ids, get_filenames_from_directory


def get_latest_file(path):
    files = get_filenames_from_directory(path, 'xml')
    return sorted(files, key=lambda x: int(x.split(';')[1]))[-1]


def has_field(field, subfield):
    field = field[0]
    for x in field:
        if x[0] == subfield:
            return True
    return False


def _get_index(author, key):
    author = author[0]
    for i, (_key, _) in enumerate(author):
        if key == _key:
            return i


def _get_orcids(xml_doc):
    result = []

    xml_authors = xml_doc.getElementsByTagName("ce:author")
    for xml_author in xml_authors:
        try:
            orcid = xml_author.getAttribute('orcid')
            result.append(orcid)
        except IndexError:
            result.append('')

    xml_authors = xml_doc.getElementsByTagName("contrib")
    for xml_author in xml_authors:
        try:
            contrib_id = xml_author.getElementsByTagName('contrib-id')[0]
            if contrib_id.getAttribute('contrib-id-type') == 'orcid':
                orcid_raw = xml_to_text(contrib_id)
                pattern = '\d\d\d\d-\d\d\d\d-\d\d\d\d-\d\d\d[\d|X]'
                result.append(re.search(pattern, orcid_raw).group())
        except (IndexError, AttributeError):
            result.append('')

    return result


def _add_orcid(record, author, field, i, orcid):
    if orcid:
        orcid = 'ORCID:{0}'.format(orcid)
        if has_field(author, 'j'):
            j = _get_index(author, 'j')
            record.warn("Amending field for orcid")
            record.amend_field((field+'__j', i, j), orcid)
        else:
            record.add_subfield((field+'__j', i, 0), 'j', orcid)


def get_file_path_by_doc_id(docid):
    filepath = "/opt/invenio/var/data/files"
    resolved_path = ""
    for subdir in listdir(filepath):
        if str(docid) in listdir(join(filepath, subdir)):
            resolved_path = join(filepath, subdir, str(docid))

    if resolved_path:
        return resolved_path
    else:
        raise MissingDocFileFolderError("Missing folder for docid: {0}".format(docid))


class MissingDocFileFolderError(Exception):
    def __init__(self, value):
        self.value = value


def check_records(records, empty=False):

    for record in records:
        doc_ids = get_doc_ids(int(record.record_id))
        for doc_id in doc_ids:
            try:
                latest_file = get_latest_file(get_file_path_by_doc_id(doc_id))
                xml = parse(latest_file)
            except:
                # DEEPLY sorry for the next line...
                continue

            orcids = _get_orcids(xml, record)
            try:
                for i, (orcid, author) in enumerate(zip(orcids[:1],
                                                        record['100'])):
                    _add_orcid(record, author, '100', i, orcid)
            except KeyError:
                pass

            try:
                for i, (orcid, author) in enumerate(zip(orcids[1:],
                                                        record['700'])):
                    _add_orcid(record, author, '700', i, orcid)
            except KeyError:
                pass
