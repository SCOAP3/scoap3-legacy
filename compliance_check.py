# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
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

import json
from string import maketrans

from invenio.bibdocfile import BibRecDocs
from invenio.rawtext_search import RawTextSearch


def get_latest_pdf(bibrec_latest_files):
    for file in bibrec_latest_files:
        if file.format == '.pdf' or file.format == '.pdf;pdfa':
            return file
    return None


def get_rawtext_from_record(record):
    bibrec = BibRecDocs(record.record_id)
    bibdoc = get_latest_pdf(bibrec.list_latest_files())
    try:
        rawtext = bibdoc.bibdoc.get_text()
    except:
        return ''
    return rawtext


def get_authors_searchterm():
    journal_list = ['iop',
                    'institute of physics',
                    'elsevier',
                    'hindawi',
                    'cas',
                    'chinese academy of science',
                    'sissa',
                    'dpg',
                    'deutsche physikalische gesellschaft',
                    'uj',
                    'jagiellonian university',
                    'oup',
                    'oxford university press',
                    'jps',
                    'physical society of japan',
                    'springer',
                    'sif',
                    'societa italiana di fisica'
                    ]

    copyright_list = ['^copyright ',
                      ' copyright ',
                      '^c ',
                      ' c ',
                      '^\(c\) ',
                      ' \(c\) ',
                      '^© ',
                      ' © '
                      ]

    joined_copyright_list = '|'.join(copyright_list)
    joined_journal_list = '|'.join(journal_list)

    regex_term = "-/(%s)/ /(%s)([0-9]* |)(to |)(%s)/" % (joined_copyright_list,
                                                         joined_copyright_list,
                                                         joined_journal_list)

    return regex_term


def check_records(records, empty=False):

    non_compliance_checks = {"CC": RawTextSearch(("-('cc-by' "
                                                  "'cc by' "
                                                  "'creative commons attribution')")),
                             "Authors": RawTextSearch(get_authors_searchterm()),
                             "SCOAP3": RawTextSearch("-'funded by scoap'")
                             }

    translation_table = maketrans('\n\t', '  ')

    for record in records:
        rawtext = get_rawtext_from_record(record)
        rawtext = rawtext.lower().translate(translation_table)
        dic = {"CC": 1, "Authors": 1, "SCOAP3": 1}
        for key, non_compliance_check in non_compliance_checks.iteritems():
            if non_compliance_check.search(rawtext):
                dic[key] = 0
        if '591' in record:
            for position, value in record.iterfield('591__a'):
                key = value[:value.find(':')]
                record.amend_field(position,
                                   '%s:%d' % (key, dic[key]),
                                   'Checking compliance.')
        else:
            for key, value in dic.iteritems():
                record.add_field('591__a',
                                 value="",
                                 subfields=[('a', '%s:%d' % (key, value))])
