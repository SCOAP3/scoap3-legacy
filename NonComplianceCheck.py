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

from string import maketrans

from invenio.rawtext_search import RawTextSearch

from invenio.utils import (get_publisher, get_rawtext_from_record_id,
                           get_filenames_from_directory)


class NonComplianceChecks:
    def __init__(self, files_path, compliance_names,
                 normal_search_delimiter="'", regex_search_delimiter="/"):
        self._non_compliance_checks = {}

        self.normal_search_delimiter = normal_search_delimiter
        self.regex_search_delimiter = regex_search_delimiter

        self._file_path = files_path
        self._translation_table = maketrans('\n\t', '  ')

        for compliance_name in compliance_names:
            self._init_non_compliance_checks(compliance_name)

    def _get_publisher_from_file_name(self, filename):
        return filename.replace('.cfg', '').split('/')[-1].split('_')[1]

    def _load_rawtext_search_from_files(self, files):
        tmp = {}

        for filename in files:
            publisher = self._get_publisher_from_file_name(filename)
            with open(filename, 'r') as f:
                lines = filter(lambda x: x != '',
                               [line.strip('\n') for line in f.readlines()])

            tmp[publisher] = RawTextSearch(lines[0].format(*lines[1:]),
                                           self.normal_search_delimiter,
                                           self.regex_search_delimiter)

        return tmp

    def _init_non_compliance_checks(self, compliance_name):
        files = get_filenames_from_directory(self._file_path,
                                             compliance_name.lower())
        tmp = self._load_rawtext_search_from_files(files)
        self._non_compliance_checks[compliance_name] = tmp

    def _get_check(self, compliance_name, publisher):
        try:
            return self._non_compliance_checks[compliance_name][publisher]
        except KeyError:
            return self._non_compliance_checks[compliance_name]['default']

    def check(self, record):
        dic = {}

        try:
            publisher = get_publisher(int(record.record_id))
        except KeyError:
            publisher = 'default'
        rawtext = (get_rawtext_from_record_id(int(record.record_id))
                   .lower().translate(self._translation_table))

        for compliance_name in self._non_compliance_checks.keys():
            dic[compliance_name] = (0 if self._get_check(compliance_name,
                                    publisher).search(rawtext) else 1)

        return dic
