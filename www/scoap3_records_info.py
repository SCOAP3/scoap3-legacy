# -*- coding: utf-8 -*-
##
## This file is part of Harvesting Kit.
## Copyright (C) 2014 CERN.
##
## Harvesting Kit is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Harvesting Kit is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Harvesting Kit; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
from invenio.search_engine import (perform_request_search,
                                   get_creation_date,
                                   get_modification_date,
                                   get_record)


JOURNALS = {'ELS/NPB': 'Nuclear Physics B',
            'ELS/PLB': 'Physics Letters B',
            'SPR/EPJC': 'European Physical Journal C',
            'SPR/JHEP': 'Journal of High Energy Physics',
            'HIN/AHEP': 'Advances in High Energy Physics',
            'OUP/PTEP': 'Progress of Theoretical and Experimental Physics',
            'IOP/CPC': 'Chinese Physics C',
            'IOP/JCAP': 'Journal of Cosmology and Astroparticle Physics',
            'IOP/NJP': 'New Journal of Physics',
            'JAG/ACTA': 'Acta'}


def index(req):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = ('attachment; filename=scoap3_records_info.csv')

    req.write("SCOAP3 record id; Journal; Creation date; Modification date; Title; Authors; Publication info\n")
    for key, value in JOURNALS.iteritems():
        recids = perform_request_search(c=value)
        for recid in recids:
            rec = get_record(recid)
            if '245' in rec:
                title = rec['245'][0][0][0][1].strip()
            else:
                title = ""
            creation_date = get_creation_date(recid)
            modification_date = get_modification_date(recid)
            if '100' in rec:
                authors = rec['100'][0][0][0][1]
            else:
                authors = ""
            if '700' in rec:
                for author in rec['700']:
                    authors += ' / %s' % (author[0][0][1])
            publication_info = ''
            if '733' in rec:
                publication_info += "%s %s (%s) %s" % (rec['733'][0][0][0][1], rec['733'][0][0][1][1], rec['733'][0][0][2][1], rec['733'][0][0][3][1])
            if '024' in rec:
                publication_info += " %s" % (rec['024'][0][0][0][1],)
            if '037' in rec:
                publication_info += " %s" % (rec['037'][0][0][0][1],)

            req.write("%s; %s; %s; %s; %s; %s; %s\n" % (recid,
                                                        value,
                                                        creation_date,
                                                        modification_date,
                                                        title,
                                                        authors,
                                                        publication_info))
