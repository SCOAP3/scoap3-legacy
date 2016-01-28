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
from collections import Iterable

from invenio.search_engine import get_record
from invenio.bibdocfile import BibRecDocs

#VARIABLES
NATIONS_DEFAULT_MAP = {"Algeria": "Algeria",
                       "Argentina": "Argentina",
                       "Armenia": "Armenia",
                       "Australia": "Australia",
                       "Austria": "Austria",
                       "Azerbaijan": "Azerbaijan",
                       "Belarus": "Belarus",
                       ##########BELGIUM########
                       "Belgium": "Belgium",
                       "Belgique": "Belgium",
                       #######################
                       "Bangladesh": "Bangladesh",
                       ##########BRAZIL#######
                       "Brazil": "Brazil",
                       "Brasil": "Brazil",
                       ######################
                       "Benin": "Republic of Benin",
                       "Bénin": "Republic of Benin",
                       "Bulgaria": "Bulgaria",
                       "Bosnia and Herzegovina": "Bosnia and Herzegovina",
                       "Canada": "Canada",
                       ##########CERN########
                       "CERN": "CERN",
                       "Cern": "CERN",
                       "European Organization for Nuclear Research": "CERN",
                       #######################
                       "Chile": "Chile",
                       ##########CHINA########
                       "China (PRC)": "China",
                       "PR China": "China",
                       "China": "China",
                       "People's Republic of China": "China",
                       #######################
                       "Colombia": "Colombia",
                       "Costa Rica": "Costa Rica",
                       "Cuba": "Cuba",
                       "Croatia": "Croatia",
                       "Northern Cyprus": "Turkey",
                       "North Cyprus": "Turkey",
                       "Cyprus": "Cyprus",
                       #######################
                       "Czech Republic": "Czech Republic",
                       "Czech": "Czech Republic",
                       #######################
                       "Denmark": "Denmark",
                       "Egypt": "Egypt",
                       "Estonia": "Estonia",
                       "Ecuador": "Ecuador",
                       "Finland": "Finland",
                       "France": "France",
                       "Georgia": "Georgia",
                       ##########GERMANY########
                       "Germany": "Germany",
                       "Deutschland": "Germany",
                       #######################
                       "Greece": "Greece",
                       ##########HONG KONG########
                       "Hong Kong": "Hong Kong",
                       "Hong-Kong": "Hong Kong",
                       #######################
                       "Hungary": "Hungary",
                       "Iceland": "Iceland",
                       "India": "India",
                       "Indonesia": "Indonesia",
                       "Iran": "Iran",
                       "Ireland": "Ireland",
                       "Israel": "Israel",
                       ##########ITALY########
                       "Italy": "Italy",
                       "Italia": "Italy",
                       #######################
                       "Japan": "Japan",
                       ##########SOUTH KOREA########
                       "Korea": "South Korea",
                       "Republic of Korea": "South Korea",
                       "South Korea": "South Korea",
                       #######################
                       "Lebanon": "Lebanon",
                       "Lithuania": "Lithuania",
                       "Luxembourg": "Luxembourg",
                       ##########MEXICO########
                       "Mexico": "Mexico",
                       "México": "Mexico",
                       #######################
                       "Monaco": "Monaco",
                       "Montenegro": "Montenegro",
                       "Morocco": "Morocco",
                       "Niger": "Niger",
                       "Nigeria": "Nigeria",
                       ##########NETHERLANDS########
                       "Netherlands": "Netherlands",
                       "The Netherlands": "Netherlands",
                       #######################
                       "New Zealand": "New Zealand",
                       "Zealand": "New Zealand",
                       #######################
                       "Norway": "Norway",
                       "Oman": "Oman",
                       "Pakistan": "Pakistan",
                       "Panama": "Panama",
                       "Poland": "Poland",
                       "Portugalo": "Portugal",
                       "Portugal": "Portugal",
                       "P.R.China": "China",
                       "Romania": "Romania",
                       ##########SAN MARINO####
                       "Republic of San Marino": "Republic of San Marino",
                       "San Marino": "Republic of San Marino",
                       ##########RUSSIA########
                       "Russia": "Russia",
                       "Russian Federation": "Russia",
                       ##########SAUDI#ARABIA##
                       "Saudi Arabia": "Saudi Arabia",
                       "Arabia": "Saudi Arabia",
                       #######################
                       "Serbia": "Serbia",
                       "Singapore": "Singapore",
                       ##########SLOVAKIA########
                       "Slovak Republic": "Slovakia",
                       "Slovak": "Slovakia",
                       "Slovakia": "Slovakia",
                       #######################
                       "Slovenia": "Slovenia",
                       ##########SOUTH AFRICA########
                       "South Africa": "South Africa",
                       "Africa": "South Africa",
                       ##############################
                       "España": "Spain",
                       "Spain": "Spain",
                       "Sudan": "Sudan",
                       "Sweden": "Sweden",
                       "Switzerland": "Switzerland",
                       "Syria": "Syria",
                       ##########TAIWAN#########
                       "Taiwan": "Taiwan",
                       "ROC": "Taiwan",
                       "R.O.C": "Taiwan",
                       "Republic of China": "Taiwan",
                       #########################
                       "Thailand": "Thailand",
                       "Tunisia": "Tunisia",
                       "Turkey": "Turkey",
                       "Ukraine": "Ukraine",
                       ##########ENGLAND########
                       "United Kingdom": "UK",
                       "Kingdom": "UK",
                       "UK": "UK",
                       "England": "UK",
                       "Scotland": "UK",
                       "Wales": "UK",
                       ##########USA########
                       "United States of America": "USA",
                       "United States": "USA",
                       "USA": "USA",
                       "America": "USA",
                       "United Sates": "USA",
                       #######################
                       "Uruguay": "Uruguay",
                       "Uzbekistan": "Uzbekistan",
                       "Venezuela": "Venezuela",
                       ##########VIETNAM########
                       "Vietnam": "Vietnam",
                       "Viet Nam": "Vietnam",
                       "Yemen": "Yemen",
                       #######################
                       #########other#########
                       "Peru": "Peru",
                       "Kuwait": "Kuwait",
                       #########SRI#LANKA#####
                       "Sri Lanka": "Sri Lanka",
                       "Lanka": "Sri Lanka",
                       #######################
                       "Kazakhstan": "Kazakhstan",
                       "Mongolia": "Mongolia",
                       #########U.Arab#Emirates#####
                       "United Arab Emirates": "United Arab Emirates",
                       "Emirates": "United Arab Emirates",
                       #######################
                       "Malaysia": "Malaysia",
                       "Qatar": "Qatar",
                       "Kyrgyz Republic": "Kyrgyz Republic",
                       "Jordan": "Jordan"}


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
