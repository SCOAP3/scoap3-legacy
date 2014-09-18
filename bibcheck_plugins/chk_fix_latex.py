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
Fixes latex for Spinger
"""
from invenio.bibrecord import record_get_field_value
import re


def strip_latex(string):
    for x in re.findall('\\\\document.*?end\{document\}', string, re.DOTALL):
        string = string.replace(x, '')

    for y in re.findall('\\\\setlength\{.*?\}\{.*?\}', string, re.DOTALL):
        string = string.replace(y, '')

    for x in re.findall('\\\\usepackage\{.*?\}', string, re.DOTALL):
        string = string.replace(x, '')

    return string.replace('  ', ' ').replace('\n', '').replace('\t', '')


def check_records(records):
    for record in records:
        publisher = record_get_field_value(record, '980', code='b')
        if publisher == 'Springer':
            title = record_get_field_value(record, '245', code='a')
            abstract = record_get_field_value(record, '520', code='a')

            title = strip_latex(title)
            abstract = strip_latex(abstract)

            for position, value in record.iterfield('245__a'):
                record.amend_field(position, title)

            for position, value in record.iterfield('520__a'):
                record.amend_field(position, abstract)

