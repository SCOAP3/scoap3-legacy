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

from os import listdir
from os.path import (isfile, join)
from collections import Iterable, OrderedDict

from invenio.search_engine import get_record
from invenio.bibdocfile import BibRecDocs

#VARIABLES
NATIONS_DEFAULT_MAP = OrderedDict()
## SPECIAL #####
NATIONS_DEFAULT_MAP["Democratic People's Republic of Korea"] = "North Korea"
NATIONS_DEFAULT_MAP["DPR Korea"] = "North Korea"
NATIONS_DEFAULT_MAP["CERN"] = "CERN"
NATIONS_DEFAULT_MAP["Cern"] = "CERN"
NATIONS_DEFAULT_MAP["European Organization for Nuclear Research"] = "CERN"
NATIONS_DEFAULT_MAP["Northern Cyprus"] = "Turkey"
NATIONS_DEFAULT_MAP["North Cyprus"] = "Turkey"
NATIONS_DEFAULT_MAP["New Mexico"] = "USA"
NATIONS_DEFAULT_MAP["Hong Kong China"] = "Hong Kong"
NATIONS_DEFAULT_MAP["Hong-Kong China"] = "Hong Kong"
## NORMAL #####
NATIONS_DEFAULT_MAP["Algeria"] = "Algeria"
NATIONS_DEFAULT_MAP["Argentina"] = "Argentina"
NATIONS_DEFAULT_MAP["Armenia"] = "Armenia"
NATIONS_DEFAULT_MAP["Australia"] = "Australia"
NATIONS_DEFAULT_MAP["Austria"] = "Austria"
NATIONS_DEFAULT_MAP["Azerbaijan"] = "Azerbaijan"
NATIONS_DEFAULT_MAP["Belarus"] = "Belarus"
NATIONS_DEFAULT_MAP["Belgium"] = "Belgium"
NATIONS_DEFAULT_MAP["Belgique"] = "Belgium"
NATIONS_DEFAULT_MAP["Bangladesh"] = "Bangladesh"
NATIONS_DEFAULT_MAP["Brazil"] = "Brazil"
NATIONS_DEFAULT_MAP["Brasil"] = "Brazil"
NATIONS_DEFAULT_MAP["Benin"] = "Republic of Benin"
NATIONS_DEFAULT_MAP["Bénin"] = "Republic of Benin"
NATIONS_DEFAULT_MAP["Bulgaria"] = "Bulgaria"
NATIONS_DEFAULT_MAP["Bolivia"] = "Bolivia"
NATIONS_DEFAULT_MAP["Bosnia and Herzegovina"] = "Bosnia and Herzegovina"
NATIONS_DEFAULT_MAP["Canada"] = "Canada"
NATIONS_DEFAULT_MAP["Chile"] = "Chile"
NATIONS_DEFAULT_MAP["China (PRC)"] = "China"
NATIONS_DEFAULT_MAP["PR China"] = "China"
NATIONS_DEFAULT_MAP["China"] = "China"
NATIONS_DEFAULT_MAP["People's Republic of China"] = "China"
NATIONS_DEFAULT_MAP["Colombia"] = "Colombia"
NATIONS_DEFAULT_MAP["Costa Rica"] = "Costa Rica"
NATIONS_DEFAULT_MAP["Cuba"] = "Cuba"
NATIONS_DEFAULT_MAP["Croatia"] = "Croatia"
NATIONS_DEFAULT_MAP["Cyprus"] = "Cyprus"
NATIONS_DEFAULT_MAP["Czech Republic"] = "Czech Republic"
NATIONS_DEFAULT_MAP["Czech"] = "Czech Republic"
NATIONS_DEFAULT_MAP["Czechia"] = "Czech Republic"
NATIONS_DEFAULT_MAP["Denmark"] = "Denmark"
NATIONS_DEFAULT_MAP["Egypt"] = "Egypt"
NATIONS_DEFAULT_MAP["Estonia"] = "Estonia"
NATIONS_DEFAULT_MAP["Ecuador"] = "Ecuador"
NATIONS_DEFAULT_MAP["Finland"] = "Finland"
NATIONS_DEFAULT_MAP["France"] = "France"
NATIONS_DEFAULT_MAP["Georgia"] = "Georgia"
NATIONS_DEFAULT_MAP["Germany"] = "Germany"
NATIONS_DEFAULT_MAP["Ghana"] = "Ghana"
NATIONS_DEFAULT_MAP["Deutschland"] = "Germany"
NATIONS_DEFAULT_MAP["Greece"] = "Greece"
NATIONS_DEFAULT_MAP["Hong Kong"] = "Hong Kong"
NATIONS_DEFAULT_MAP["Hong-Kong"] = "Hong Kong"
NATIONS_DEFAULT_MAP["Hungary"] = "Hungary"
NATIONS_DEFAULT_MAP["Iceland"] = "Iceland"
NATIONS_DEFAULT_MAP["India"] = "India"
NATIONS_DEFAULT_MAP["Indonesia"] = "Indonesia"
NATIONS_DEFAULT_MAP["Iran"] = "Iran"
NATIONS_DEFAULT_MAP["Ireland"] = "Ireland"
NATIONS_DEFAULT_MAP["Israel"] = "Israel"
NATIONS_DEFAULT_MAP["Italy"] = "Italy"
NATIONS_DEFAULT_MAP["Italia"] = "Italy"
NATIONS_DEFAULT_MAP["Japan"] = "Japan"
NATIONS_DEFAULT_MAP["Jamaica"] = "Jamaica"
NATIONS_DEFAULT_MAP["Korea"] = "South Korea"
NATIONS_DEFAULT_MAP["Republic of Korea"] = "South Korea"
NATIONS_DEFAULT_MAP["South Korea"] = "South Korea"
NATIONS_DEFAULT_MAP["Latvia"] = "Latvia"
NATIONS_DEFAULT_MAP["Lebanon"] = "Lebanon"
NATIONS_DEFAULT_MAP["Lithuania"] = "Lithuania"
NATIONS_DEFAULT_MAP["Luxembourg"] = "Luxembourg"
NATIONS_DEFAULT_MAP["Macedonia"] = "Macedonia"
NATIONS_DEFAULT_MAP["Malta"] = "Malta"
NATIONS_DEFAULT_MAP["Mexico"] = "Mexico"
NATIONS_DEFAULT_MAP["México"] = "Mexico"
NATIONS_DEFAULT_MAP["Monaco"] = "Monaco"
NATIONS_DEFAULT_MAP["Montenegro"] = "Montenegro"
NATIONS_DEFAULT_MAP["Morocco"] = "Morocco"
NATIONS_DEFAULT_MAP["Niger"] = "Niger"
NATIONS_DEFAULT_MAP["Nigeria"] = "Nigeria"
NATIONS_DEFAULT_MAP["Netherlands"] = "Netherlands"
NATIONS_DEFAULT_MAP["The Netherlands"] = "Netherlands"
NATIONS_DEFAULT_MAP["New Zealand"] = "New Zealand"
NATIONS_DEFAULT_MAP["Zealand"] = "New Zealand"
NATIONS_DEFAULT_MAP["Norway"] = "Norway"
NATIONS_DEFAULT_MAP["Oman"] = "Oman"
NATIONS_DEFAULT_MAP["Pakistan"] = "Pakistan"
NATIONS_DEFAULT_MAP["Panama"] = "Panama"
NATIONS_DEFAULT_MAP["Palestine"] = "Palestine"
NATIONS_DEFAULT_MAP["Philippines"] = "Philippines"
NATIONS_DEFAULT_MAP["Poland"] = "Poland"
NATIONS_DEFAULT_MAP["Portugalo"] = "Portugal"
NATIONS_DEFAULT_MAP["Portugal"] = "Portugal"
NATIONS_DEFAULT_MAP["P.R.China"] = "China"
NATIONS_DEFAULT_MAP["Romania"] = "Romania"
NATIONS_DEFAULT_MAP["Republic of San Marino"] = "Republic of San Marino"
NATIONS_DEFAULT_MAP["San Marino"] = "Republic of San Marino"
NATIONS_DEFAULT_MAP["Russia"] = "Russia"
NATIONS_DEFAULT_MAP["Russian Federation"] = "Russia"
NATIONS_DEFAULT_MAP["Saudi Arabia"] = "Saudi Arabia"
NATIONS_DEFAULT_MAP["Arabia"] = "Saudi Arabia"
NATIONS_DEFAULT_MAP["Serbia"] = "Serbia"
NATIONS_DEFAULT_MAP["Singapore"] = "Singapore"
NATIONS_DEFAULT_MAP["Slovak Republic"] = "Slovakia"
NATIONS_DEFAULT_MAP["Slovak"] = "Slovakia"
NATIONS_DEFAULT_MAP["Slovakia"] = "Slovakia"
NATIONS_DEFAULT_MAP["Slovenia"] = "Slovenia"
NATIONS_DEFAULT_MAP["South Africa"] = "South Africa"
NATIONS_DEFAULT_MAP["Africa"] = "South Africa"
NATIONS_DEFAULT_MAP["España"] = "Spain"
NATIONS_DEFAULT_MAP["Spain"] = "Spain"
NATIONS_DEFAULT_MAP["Sudan"] = "Sudan"
NATIONS_DEFAULT_MAP["Sweden"] = "Sweden"
NATIONS_DEFAULT_MAP["Switzerland"] = "Switzerland"
NATIONS_DEFAULT_MAP["Syria"] = "Syria"
NATIONS_DEFAULT_MAP["Taiwan"] = "Taiwan"
NATIONS_DEFAULT_MAP["ROC"] = "Taiwan"
NATIONS_DEFAULT_MAP["R.O.C"] = "Taiwan"
NATIONS_DEFAULT_MAP["Republic of China"] = "Taiwan"
NATIONS_DEFAULT_MAP["Thailand"] = "Thailand"
NATIONS_DEFAULT_MAP["Tunisia"] = "Tunisia"
NATIONS_DEFAULT_MAP["Turkey"] = "Turkey"
NATIONS_DEFAULT_MAP["Ukraine"] = "Ukraine"
NATIONS_DEFAULT_MAP["United Kingdom"] = "UK"
NATIONS_DEFAULT_MAP["Kingdom"] = "UK"
NATIONS_DEFAULT_MAP["UK"] = "UK"
NATIONS_DEFAULT_MAP["England"] = "UK"
NATIONS_DEFAULT_MAP["Scotland"] = "UK"
NATIONS_DEFAULT_MAP["Wales"] = "UK"
NATIONS_DEFAULT_MAP["United States of America"] = "USA"
NATIONS_DEFAULT_MAP["United States"] = "USA"
NATIONS_DEFAULT_MAP["USA"] = "USA"
NATIONS_DEFAULT_MAP["America"] = "USA"
NATIONS_DEFAULT_MAP["United Sates"] = "USA"
NATIONS_DEFAULT_MAP["Uruguay"] = "Uruguay"
NATIONS_DEFAULT_MAP["Uzbekistan"] = "Uzbekistan"
NATIONS_DEFAULT_MAP["Venezuela"] = "Venezuela"
NATIONS_DEFAULT_MAP["Vietnam"] = "Vietnam"
NATIONS_DEFAULT_MAP["Viet Nam"] = "Vietnam"
NATIONS_DEFAULT_MAP["Yemen"] = "Yemen"
NATIONS_DEFAULT_MAP["Peru"] = "Peru"
NATIONS_DEFAULT_MAP["Kuwait"] = "Kuwait"
NATIONS_DEFAULT_MAP["Sri Lanka"] = "Sri Lanka"
NATIONS_DEFAULT_MAP["Lanka"] = "Sri Lanka"
NATIONS_DEFAULT_MAP["Kazakhstan"] = "Kazakhstan"
NATIONS_DEFAULT_MAP["Mongolia"] = "Mongolia"
NATIONS_DEFAULT_MAP["United Arab Emirates"] = "United Arab Emirates"
NATIONS_DEFAULT_MAP["UAE"] = "United Arab Emirates"
NATIONS_DEFAULT_MAP["Emirates"] = "United Arab Emirates"
NATIONS_DEFAULT_MAP["Malaysia"] = "Malaysia"
NATIONS_DEFAULT_MAP["Qatar"] = "Qatar"
NATIONS_DEFAULT_MAP["Kyrgyz Republic"] = "Kyrgyz Republic"
NATIONS_DEFAULT_MAP["Jordan"] = "Jordan"
## cities #############
NATIONS_DEFAULT_MAP['Belgrade'] = 'Serbia'
NATIONS_DEFAULT_MAP['Istanbul'] = 'Turkey'
NATIONS_DEFAULT_MAP['Ankara'] = 'Turkey'
NATIONS_DEFAULT_MAP['Rome'] = 'Italy'
NATIONS_DEFAULT_MAP['INFN'] = 'Italy'
NATIONS_DEFAULT_MAP['Triumf'] = 'USA'


#SCOAP3 related
def get_doi(recid):
    return sorted(get_record(recid)['024'][0][0],
                  key=lambda x: 1 if x[0] == 'a' else 2)[0][1]


def get_doc_ids(recid):
    return [bibdoc.get_id() for bibdoc in BibRecDocs(recid).list_bibdocs()]


def get_arxiv(recid):
    return sorted(get_record(recid)['037'][0][0],
                  key=lambda x: 1 if x[0] == 'a' else 2)[0][1]


def get_publisher(recid):
    return sorted(get_record(recid)['773'][0][0],
                  key=lambda x: 1 if x[0] == 'a' else 2)[0][1]


def get_latest_pdf(bibrec_latest_files):
    for file in bibrec_latest_files:
        if file.format == '.pdf' or file.format == '.pdf;pdfa':
            return file
    return None


def get_rawtext_from_record_id(record_id):
    bibrec = BibRecDocs(record_id)
    bibdoc = get_latest_pdf(bibrec.list_latest_files())
    try:
        rawtext = bibdoc.bibdoc.get_text()
    except:
        return ''

    return rawtext


#GENERAL
def get_filenames_from_directory(dirname, _filter=''):
    return [join(dirname, f) for f in listdir(dirname)
            if isfile(join(dirname, f)) and _filter in f]


def flatten_list(l):
    tmp = []
    if isinstance(l, Iterable) and not isinstance(l, basestring):
        for sl in l:
            tmp.extend(flatten_list(sl))
    else:
        return [l]

    return tmp


def multi_replace(s, replaces):
        for old, new in replaces:
            s = s.replace(old, new)
        return s


def build_path(file_path):
    pass


def split_path(file_path):
    pass
