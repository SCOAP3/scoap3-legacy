# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""SCOAP3 frontpage UI."""

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template
from invenio_search.api import current_search_client
from invenio_collections.models import Collection

blueprint = Blueprint(
    'scoap3_home',
    __name__,
    template_folder='templates',
    static_folder='static',
)

@blueprint.route('/')
def index():
    """SCOAP3 home page."""

    count = current_search_client.count(index='records-record')
    collections = Collection.query.filter(Collection.level == 2, Collection.parent_id == 1).all()
    for collection in collections:
        collection.count = current_search_client.count(q='_collections:"%s"' % (collection.name,))['count']

    # # TODO show only for administrators
    # publishers = [{'name':'Elsevier'},
    #               {'name':'Jagiellonian University'},
    #               {'name':'Hindawi'},
    #               {'name':u'Springer/Società Italiana di Fisica'},
    #               {'name':'Springer/SISSA'},
    #               {'name':'Institute of Physics Publishing/SISSA'},
    #               {'name':'Institute of Physics Publishing/Deutsche Physikalische Gesellschaft'},
    #               {'name':'Institute of Physics Publishing/Chinese Academy of Sciences'},
    #               {'name':'Oxford University Press/Physical Society of Japan'}]
    # for publisher in publishers:
    #     publisher['count'] = current_search_client.count(q=u'imprints.publisher:"{0}"'.format(publisher['name']))['count']
    #TODO Move to configuration
    countries = ["Australia","Austria", "Belgium", "Canada", "China", "CERN",
                 "Czech Republic", "Denmark", "Finland", "France", "Germany",
                 "Greece", "Hong-Kong", "Hungary", "Iceland", "Israel",
                 "Italy", "Japan", "JINR", "South Korea", "Mexico",
                 "Netherlands", "Norway", "Poland", "Portugal",
                 "Slovak Republic", "South Africa", "Spain", "Sweden",
                 "Switzerland", "Taiwan", "Turkey", "United Kingdom",
                 "United States"]
    countries = {country:{'search_names':[country]} for country in countries}
    countries['Hong-Kong']['search_names'] = ['Hong Kong']
    countries['Slovak Republic']['search_names'] = ['Slovakia']
    countries['United Kingdom']['search_names'] = ['UK']
    countries['United States']['search_names'] = ['USA']
    countries['JINR']['search_names'] = ['Armenia', 'Azerbaijan', 'Belarus',
                                        'Cuba', 'North Korea', 'Georgia',
                                        'Kazakhstan', 'Moldova', 'Mongolia',
                                        'Ukraine', 'Uzbekistan', 'Vietnam']

    for country in countries:
        query = ''
        for name in countries[country]['search_names']:
            if query:
                query += " or "
            query += 'country:"{0}"'.format(name)
        countries[country]['query'] = query
        countries[country]['count'] = current_search_client.count(q=query)['count']

    return render_template(
        'scoap3_frontpage/home.html',
        title='SCOAP3 Repository',
        articles_count=count['count'],
        collections=sorted(collections, key=lambda x: x.name),
        countries=countries
    )
