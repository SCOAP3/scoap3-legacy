from invenio.webpage import pagefooteronly, pageheaderonly
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
            title = rec['245'][0][0][0][1].strip()
            creation_date = get_creation_date(recid)
            modification_date = get_modification_date(recid)
            authors = rec['100'][0][0][0][1]
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


            req.writeline("%s; %s; %s; %s; %s; %s; %s\n" % (recid,
                                                            value,
                                                            creation_date,
                                                            modification_date,
                                                            title,
                                                            authors,
                                                            publication_info))
