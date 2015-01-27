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

from xml.dom.minidom import parse

from harvestingkit.utils import add_nations_field
from harvestingkit.minidom_utils import xml_to_text, get_value_in_tag
from invenio.utils import get_doc_ids, get_filenames_from_directory


def is_elsevier(record):
    fields = ['980', '260']
    for field in fields:
        if field in record:
            for values in record[field][0][0]:
                if 'Elsevier' in values:
                    return True
    return False


def author_dic_from_xml(author):
    tmp = {}
    surname = get_value_in_tag(author, "ce:surname")
    if surname:
        tmp["surname"] = surname
    given_name = get_value_in_tag(author, "ce:given-name")
    if given_name:
        tmp["given_name"] = given_name
    initials = get_value_in_tag(author, "ce:initials")
    if initials:
        tmp["initials"] = initials
    orcid = author.getAttribute('orcid').encode('utf-8')
    if orcid:
        tmp["orcid"] = orcid
    emails = author.getElementsByTagName("ce:e-address")
    for email in emails:
        if email.getAttribute("type").encode('utf-8') in ('email', ''):
            tmp["email"] = xml_to_text(email)
            break
    cross_refs = author.getElementsByTagName("ce:cross-ref")
    if cross_refs:
        tmp["cross_ref"] = []
        for cross_ref in cross_refs:
            tmp["cross_ref"].append(
                cross_ref.getAttribute("refid").encode('utf-8'))

    return tmp


def _affiliation_from_sa_field(affiliation):
    sa_aff = affiliation.getElementsByTagName('sa:affiliation')[0]
    return xml_to_text(sa_aff, ', ')


def find_affiliations(xml_doc):
    tmp = {}
    for aff in xml_doc.getElementsByTagName("ce:affiliation"):
        aff_id = aff.getAttribute("id").encode('utf-8')
        try:
            tmp[aff_id] = _affiliation_from_sa_field(aff)
        except:
            tmp[aff_id] = re.sub(r'^(\d+\ ?)', "",
                                 get_value_in_tag(aff, "ce:textfn"))

    return tmp


def _add_affiliations(author, affs):
    if affs:
        try:
            author['affiliation'].extend(affs)
        except KeyError:
            author['affiliation'] = affs

    return len(affs)


def add_referenced_affiliation(author, affiliations):
    affs = [affiliations[ref] for ref in author.get("cross_ref", [])
            if ref in affiliations]

    return _add_affiliations(author, affs)


def add_group_affiliation(author, xml_author):
    affs = [get_value_in_tag(aff, "ce:textfn") for aff
            in xml_author.parentNode.getElementsByTagName('ce:affiliation')]

    return _add_affiliations(author, affs)


def get_direct_cildren(element, tagname):
    affs = []
    for child in element.childNodes:
        try:
            if child.tagName == tagname:
                affs.append(child)
        except AttributeError:
            pass
    return affs


def add_global_affiliation(author, xml_author):
    affs = []
    # get author group of author, but this is already done in group_affiliation
    parent = xml_author.parentNode
    while True:
        try:
            parent = parent.parentNode
            affs.extend([get_value_in_tag(aff, "ce:textfn") for aff
                         in get_direct_cildren(parent, 'ce:affiliation')])
        except AttributeError:
            break

    return _add_affiliations(author, affs)


def add_affiliations(authors, xml_authors, affiliations):
    for xml_author, author in zip(xml_authors, authors):
        if not add_referenced_affiliation(author, affiliations):
            add_group_affiliation(author, xml_author)
        add_global_affiliation(author, xml_author)


def get_authors(xml_doc):
        xml_authors = xml_doc.getElementsByTagName("ce:author")
        authors = [author_dic_from_xml(author) for author in xml_authors]

        add_affiliations(authors, xml_authors, find_affiliations(xml_doc))

        return authors


def get_latest_file(path):
    files = get_filenames_from_directory(path, 'xml')
    return sorted(files, key=lambda x: int(x.split(';')[1]))[-1]


def delete_fields(record, fields):
    for field in fields:
        try:
            del record[field]
        except KeyError:
            pass


def check_records(records, empty=False):
    fields = ['100', '700']
    filepath = "/opt/invenio/var/data/files/g0/"
    filepath2 = "/opt/invenio/var/data/files/g1/"
    first_author = True

    for record in records:
        if is_elsevier(record):
            doc_ids = get_doc_ids(int(record.record_id))
            for doc_id in doc_ids:
                try:
                    latest_file = get_latest_file(filepath + str(doc_id) + '/')
                except:
                    latest_file = get_latest_file(filepath2 + str(doc_id) + '/')
                try:
                    xml = parse(latest_file)
                except:
                    record.warn("Problem parssing XML file. Aborting")
                    break
                authors = get_authors(xml)

                delete_fields(record, fields)

                for author in authors:
                    field = '100' if first_author else '700'
                    first_author = False

                    subfields = []
                    author_name = (author['surname'], author.get(
                        'given_name') or author.get('initials'))
                    author_name = ('a', '%s, %s' % author_name)
                    subfields.append(author_name)

                    if 'orcid' in author:
                        subfields.append(('j', author['orcid']))

                    if 'affiliation' in author:
                        for aff in author["affiliation"]:
                            subfields.append(('v', aff))

                        add_nations_field(subfields)

                    if author.get('email'):
                        subfields.append(('m', author['email']))

                    record.add_field(field+'__',
                                     value='',
                                     subfields=subfields)
