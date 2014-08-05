# -*- coding: utf-8 -*-
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
                       "México": "México",
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


def find_nations(field, subfields):
    all_aff_string = ''
    for x in field:
        if x[0] in subfields:
            all_aff_string += x[1] + ', '

    all_aff = [x.replace('.', '') for x in all_aff_string.split(', ')]

    return map(NATIONS_DEFAULT_MAP.get,
               filter(lambda x: x in all_aff, NATIONS_DEFAULT_MAP.keys()))


def has_field(field, subfield):
    for x in field:
        if x[0] == subfield:
            return True
    return False


def check_records(records, empty=False):
    fields = ['100', '700']

    for record in records:
        for field in fields:
            if field in record:
                for i, x in enumerate(record[field]):
                    data = x[0]
                    if not has_field(data, 'w'):
                        nations = find_nations(data, ['u', 'v'])
                        if len(nations) == 1:
                            val = nations[0]
                        else:
                            val = 'HUMAN CHECK'
                        record.add_subfield((field + '__w', i, 0), 'w', val)
