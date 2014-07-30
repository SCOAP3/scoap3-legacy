from os import listdir
from os.path import isfile

from string import maketrans

from invenio.rawtext_search import RawTextSearch

from invenio.utils import (get_publisher, get_rawtext_from_record_id,
                           get_filenames_from_directory)


class NonComplianceChecks:
    def __init__(self, files_path, compliance_names):
        self._non_compliance_checks = {}

        self._file_path = files_path
        self._translation_table = maketrans('\n\t', '  ')

        for compliance_name in compliance_names:
            self._init_non_compliance_checks(compliance_name)

    def _get_publisher_from_file_name(self, filename):
        return filename.replace('.cfg', '').split('_')[1]

    def _load_rawtext_search_from_files(self, files):
        tmp = {}

        for filename in files:
            publisher = self._get_publisher_from_file_name(filename)
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f.readlines()]

            tmp[publisher] = RawTextSearch(lines[0].format(*lines[1:]))

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

        publisher = get_publisher(record.record_id)
        rawtext = (get_rawtext_from_record_id(record.record_id)
                   .lower().translate(self._translation_table))

        for compliance_name in self._non_compliance_checks.keys():
            dic[compliance_name] = (0 if self._get_check(compliance_name,
                                    publisher).search(rawtext) else 1)

        return dic
