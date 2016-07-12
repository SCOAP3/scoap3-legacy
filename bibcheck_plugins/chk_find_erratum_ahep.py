## This file is part of SCOAP3.
## Copyright (C) 2015 CERN.
##
## SCOAP3 is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## SCOAP3 is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with SCOAP3; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Finds paper in AHEP which are erratum, addendum, edditorial or corrigendum and
assigns them an extra collection: ERRATUM, ADDENDUM ,EDITORIAL or CORRIGENDUM.
"""
from invenio.bibdocfile import BibRecDocs
import xml.dom.minidom
from harvestingkit.minidom_utils import get_value_in_tag
from invenio.bibrecord import record_get_field_value

def check_records(records):
    for record in records:
        ## Stupid hack because bibcheck filters does not work as expected
        if record_get_field_value(record, '980', code='b') == "Hindawi":
            record.warn("Working on this record")
            recdoc = BibRecDocs(int(record.record_id))
            doc = recdoc.get_bibdoc(recdoc.get_bibdoc_names()[0])
            try:
                xml_file = open(doc.get_file("xml").get_full_path())
            except:
                record.warn("No document can be found")
                continue
            xml2 = xml.dom.minidom.parseString(xml_file.read())
            subject = get_value_in_tag(xml2, "subject")
            if subject in ["Editorial", "Erratum", "Corrigendum", "Addendum","Letter to the Editor"]:
                field = record_get_field_value(record, '980', code='c')
                if field:
                    if field in ['ERRATUM', 'ADDENDUM', 'EDITORIAL','CORRIGENDUM', 'LETTER TO THE EDITOR']:
                        for position, value in record.iterfield('980__c'):
                            record.amend_field(position, subject.upper())
                            break
                    else:
                        for position, value in record.iterfield('980__%'):
                            record.add_subfield(position, 'c', subject.upper())
                            break
                else:
                    for position, value in record.iterfield('980__%'):
                        record.add_subfield(position, 'c', subject.upper())
                        break
            elif subject not in ["Review Article","Research Article","Retraction"]:
                raise Exception("This subject: %s does not exit in SCOAP3 system" % (subject,))

