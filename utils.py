# -*- coding: utf-8 -*-
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
                       "Brazil": "Brazil",
                       "Bulgaria": "Bulgaria",
                       "Canada": "Canada",
                       "Chile": "Chile",
                       ##########CHINA########
                       "China (PRC)": "China",
                       "PR China": "China",
                       "China": "China",
                       #######################
                       "Colombia": "Colombia",
                       "Costa Rica": "Costa Rica",
                       "Cuba": "Cuba",
                       "Croatia": "Croatia",
                       "Cyprus": "Cyprus",
                       "Czech Republic": "Czech Republic",
                       "Denmark": "Denmark",
                       "Egypt": "Egypt",
                       "Estonia": "Estonia",
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
                       ##########MEXICO########
                       "Mexico": "Mexico",
                       "México": "Mexico",
                       #######################
                       "Montenegro": "Montenegro",
                       "Morocco": "Morocco",
                       ##########NETHERLANDS########
                       "Netherlands": "Netherlands",
                       "The Netherlands": "Netherlands",
                       #######################
                       "New Zealand": "New Zealand",
                       "Norway": "Norway",
                       "Pakistan": "Pakistan",
                       "Poland": "Poland",
                       "Portugal": "Portugal",
                       "Romania": "Romania",
                       ##########RUSSIA########
                       "Russia": "Russia",
                       "Russian Federation": "Russia",
                       #######################
                       "Saudi Arabia": "Saudi Arabia",
                       "Serbia": "Serbia",
                       "Singapore": "Singapore",
                       "Slovak Republic": "Slovakia",
                       ##########SLOVAKIA########
                       "Slovakia": "Slovakia",
                       "Slovenia": "Slovenia",
                       #######################
                       "South Africa": "South Africa",
                       "Spain": "Spain",
                       "Sweden": "Sweden",
                       "Switzerland": "Switzerland",
                       "Taiwan": "Taiwan",
                       "Thailand": "Thailand",
                       "Tunisia": "Tunisia",
                       "Turkey": "Turkey",
                       "Ukraine": "Ukraine",
                       ##########ENGLAND########
                       "United Kingdom": "UK",
                       "UK": "UK",
                       #######################
                       "England": "England",
                       ##########USA########
                       "United States of America": "USA",
                       "United States": "USA",
                       "USA": "USA",
                       #######################
                       "Uruguay": "Uruguay",
                       "Uzbekistan": "Uzbekistan",
                       "Venezuela": "Venezuela",
                       ##########VIETNAM########
                       "Vietnam": "Vietnam",
                       "Viet Nam": "Vietnam",
                       #######################
                       #########other#########
                       "Peru": "Peru",
                       "Kuwait": "Kuwait",
                       "Sri Lanka": "Sri Lanka",
                       "Kazakhstan": "Kazakhstan",
                       "Mongolia": "Mongolia",
                       "United Arab Emirates": "United Arab Emirates",
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
