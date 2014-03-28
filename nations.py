from cgi import escape
from urllib import urlencode

from invenio.webinterface_handler_config import HTTP_BAD_REQUEST, SERVER_RETURN
from invenio.webpage import pagefooteronly, pageheaderonly, page
from invenio.search_engine import perform_request_search
from invenio.search_engine import get_coll_i18nname, get_record, get_collection_reclist
from invenio.bibrecord import record_get_field_value
from invenio.dbquery import run_sql


_CFG_NATION_MAP = [("Algeria", ),
                   ("Argentina", ),
                   ("Armenia", ),
                   ("Australia", ),
                   ("Austria", ),
                   ("Azerbaijan", ),
                   ("Belarus", ),
                   ("Belgium", "Belgique"),
                   ("Bangladesh", ),
                   ("Brazil", ),
                   ("Bulgaria", ),
                   ("Canada", ),
                   ("CERN", ),
                   ("Chile", ),
                   ("China (PRC)", "PR China", "China"),
                   ("Colombia", ),
                   ("Costa Rica", ),
                   ("Croatia", ),
                   ("Cuba", ),
                   ("Cyprus", ),
                   ("Czech Republic", ),
                   ("Denmark", ),
                   ("Egypt", ),
                   ("Estonia", ),
                   ("Finland", ),
                   ("France", ),
                   ("Georgia", ),
                   ("Germany", "Deutschland"),
                   ("Greece", ),
                   ("Hong-Kong", "Hong Kong"),
                   ("Hungary", ),
                   ("Iceland", ),
                   ("India", ),
                   ("Indonesia", ),
                   ("Iran", ),
                   ("Ireland", ),
                   ("Israel", ),
                   ("Italy", "Italia"),
                   ("Japan", ),
                   ("Korea", "Republic of Korea", "South Korea"),
                   ("Lebanon", ),
                   ("Lithuania", ),
                   ("México", "Mexico"),
                   ("Montenegro", ),
                   ("Morocco", ),
                   ("Netherlands", "The Netherlands"),
                   ("New Zealand", ),
                   ("Norway", ),
                   ("Pakistan", ),
                   ("Poland", ),
                   ("Portugal", ),
                   ("Romania", ),
                   ("Russia", "Russian Federation"),
                   ("Saudi Arabia", ),
                   ("Serbia", ),
                   ("Singapore", ),
                   ("Slovak Republic", "Slovakia"),
                   ("Slovenia", ),
                   ("South Africa", ),
                   ("Spain", ),
                   ("Sweden", ),
                   ("Switzerland", ),
                   ("Taiwan", ),
                   ("Thailand", ),
                   ("Tunisia", ),
                   ("Turkey", ),
                   ("Ukraine", ),
                   ("United Kingdom", "UK", "U.K", "England"),
                   ("United States of America", "United States", "USA", "U.S.A"),
                   ("Uruguay", ),
                   ("Uzbekistan", ),
                   ("Venezuela", ),
                   ("Vietnam", "Viet Nam"),
                   ## ------ other -----
                   ("Peru", ),
                   ("Kuwait", ),
                   ("Sri Lanka", ),
                   ("Kazakhstan", ),
                   ("Mongolia", ),
                   ("United Arab Emirates", ),
                   ("Malaysia", ),
                   ("Qatar", ),
                   ("Kyrgyz Republic", ),
                   ("Jordan", )]

CFG_JOURNALS = ['Acta',
                'Advances in High Energy Physics',
                'Chinese Physics C',
                'European Physical Journal C',
                'Journal of Cosmology and Astroparticle Physics',
                'Journal of High Energy Physics',
                'New Journal of Physics',
                'Nuclear Physics B',
                'Physics Letters B',
                'Progress of Theoretical and Experimental Physics']

CFG_SELECTED_AFF = {'Andrews University': ('Andrews University',),
                    'Arkansas State University': ('Arkansas State University',),
                    'Auburn University': ('Auburn University',),
                    'Black Hills State University': ('Black Hills State University',),
                    'Boise State University': ('Boise State University',),
                    'Brookhaven National Laboratory': ('Brookhaven National Laboratory',),
                    'Brown University': ('Brown University',),
                    'Chicago State University': ('Chicago State University',),
                    'Colorado State University': ('Colorado State University',),
                    'Columbia University': ('Columbia University',),
                    'Creighton University': ('Creighton University',),
                    'Fairfield University': ('Fairfield University',),
                    'George Washington University': ('George Washington University',),
                    'Hampton University': ('Hampton University',),
                    'Houston Advanced Research Center': ('Houston Advanced Research Center',),
                    'Howard University': ('howard university',),
                    'Janelia Farm Research Campus': ('Janelia Farm Research Campus',),
                    'Long Island University': ('Long Island University',),
                    'Louisiana Tech University': ('Louisiana Tech University',),
                    'Luther College': ('Luther College',),
                    'Manhattan College': ('Manhattan College',),
                    'Milwaukee School of Engineering': ('Milwaukee School of Engineering',),
                    'Mississippi State University': ('Mississippi State University',),
                    'Muhlenberg College': ('Muhlenberg College',),
                    'New York City College of Technology': ('New York City College of Technology',),
                    'North Carolina Central University': ('North Carolina Central University',),
                    'Northern Illinois University': ('Northern Illinois University',),
                    'Oklahoma State University': ('Oklahoma State University',),
                    'Oklahoma State': ('Oklahoma State',),
                    'Pacific Lutheran University': ('Pacific Lutheran University',),
                    'Philander Smith College': ('Philander Smith College',),
                    'Rutgers University': ('Rutgers University',),
                    'Rutgers': ('Rutgers University',),
                    'South Dakota School of Mines and Technology': ('South Dakota School of Mines and Tec',),
                    'Southern Illinois University Carbondale': ('southern illinois university', 'carbondale'),
                    'Stanford University': ('Stanford University',),
                    'State University of New York (or SUNY) Albany': ('SUNY Albany', 'University at Albany (SUNY)', 'Albany'),
                    'State University of New York (or SUNY) Buffalo': ('University at Buffalo', 'State University of New York at Buffalo'),
                    'Syracuse University': ('Syracuse University',),
                    'Techas Tech University': ('texas tech',),
                    'Tennessee Tech University': ('Tennessee Tech University',),
                    'Texas Tech University': ('Texas Tech University',),
                    'The George Washington University': ('The George Washington University',),
                    'The Graduate School and University Center, The City University of New York': ('The Graduate School and University Center, The City University o',),
                    'The Rockefeller University': ('The Rockefeller University',),
                    'The University of Alabama, Tuscaloosa': ('The University of Alabama, Tuscaloosa',),
                    'The University of Mississippi': ('The University of Mississippi',),
                    'Triangle Universities Nuclear Laboratory': ('Triangle Universities Nuclear Laboratory',),
                    'University of Connecticut': ('University of Connecticut',),
                    'University of Delaware': ('University of Delaware',),
                    'University of Hawaii': ('university of hawaii',),
                    'University of Hawaii': ('University of Hawaii',),
                    'University of Houston': ('University of Houston',),
                    'University of Louisville': ('University of Luisville',),
                    'University of Puerto Rico': ('University of Puerto Rico',),
                    'University of South Dakota': ('University of South Dakota',),
                    'Utah Valley University': ('Utah Valley University',),
                    'Virginia Military Institute': ('Virginia Military Institute',),
                    'Wayne State University': ('Wayne State University',),
                    'Wayne University': ('Wayne State university',),
                    'Western Michigan University': ('Western Michigan University',),
                    'Yale University': ('Yale University',)}


def _build_query(nation_tuple):
    out = []
    for value in nation_tuple:
        out.append('affiliation:"*%s" OR affiliation:"*%s."' % (value, value))
    return " OR ".join(out)


def index(req):
    req.content_type = "text/html"
    req.write(pageheaderonly("Nation numbers", req=req))
    req.write("<h1>Nation numbers</h1>")
    req.flush()
    req.write("<table>\n")
    for i, nation_tuple in enumerate(_CFG_NATION_MAP):
        query = _build_query(nation_tuple)
        results = perform_request_search(p=query, of='intbitset')
        req.write("""<tr><td>%s</td><td><a href="/search?%s&sc=1">%s</a></td><td><a href="/nations.py/articles?i=%s" target="_blank">Articles</a> (<a href="/nations.py/articles?mode=text&amp;i=%s">text</a>)</td><tr>\n""" % (
                escape(nation_tuple[0]), escape(urlencode([("p", query)]), True), len(results), i, i
            ))
        req.flush()
    req.write("</table>\n")
    req.write(pagefooteronly(req=req))
    return ""


def late(req):
    req.content_type = "text/html"
    print >> req, pageheaderonly("Late journals", req=req)
    for journal in CFG_JOURNALS:
        print >> req, "<h2>%s</h2>" % escape(get_coll_i18nname(journal))
        results = get_collection_reclist(journal)
        print >> req, "<table>"
        print >> req, "<tr><th>DOI</th><th>Title</th><th>DOI registration</th><th>Arrival in SCOAP3</th></tr>"
        for recid in results:
            creation_date = run_sql("SELECT creation_date FROM bibrec WHERE id=%s", (recid, ))[0][0]
            record = get_record(recid)
            doi = record_get_field_value(record, '024', '7', code='a')
            title = record_get_field_value(record, '245', code='a')
            doi_date = run_sql("SELECT creation_date FROM doi WHERE doi=%s", (doi, ))
            background = "#eee"
            if doi_date:
                doi_date = doi_date[0][0]
                if (creation_date - doi_date).days < 0:
                    background = "#66FF00"
                elif (creation_date - doi_date).days < 1:
                    background = "#FF6600"
                else:
                    background = "#FF0000"
            else:
                doi_date = ''
            print >> req, '<tr style="background-color: %s;"><td><a href="http://dx.doi.org/%s" target="_blank">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                    background,
                    escape(doi, True),
                    escape(doi),
                    title,
                    doi_date,
                    creation_date)
        print >> req, "</table>"


def articles(req, i, mode='html'):
    try:
        i = int(i)
        assert 0 <= i < len(_CFG_NATION_MAP)
    except:
        raise SERVER_RETURN(HTTP_BAD_REQUEST)
    nation_tuple = _CFG_NATION_MAP[i]
    ret = []
    page_title = "SCOAP3 Articles by authors from %s" % nation_tuple[0]
    if mode == 'text':
        req.content_type = "text/plain; charset=utf8"
        req.headers_out['content-disposition'] = 'attachment; filename=%s.txt' % nation_tuple[0]
    else:
        req.content_type = "text/html"
    if mode == 'text':
        print >> req, page_title
        print >> req, "-" * len(page_title)
    query = _build_query(nation_tuple)
    for journal in CFG_JOURNALS:
        results = perform_request_search(p=query, cc=journal, of='intbitset')
        if not results:
            #ret.append("<p>No articles yet</p>")
            continue
        ret.append("<h2>%s (%s)</h2" % (escape(get_coll_i18nname(journal)), len(results)))
        ret.append("<p><ul>")
        if mode == 'text':
            print >> req, ""
            print >> req, get_coll_i18nname(journal)
        for recid in results:
            record = get_record(recid)
            title = record_get_field_value(record, '245', code='a')
            doi = record_get_field_value(record, '024', '7', code='a')
            if mode == 'text':
                print >> req, "http://dx.doi.org/%s" % doi
            ret.append('<li><a href="http://dx.doi.org/%s" target="_blank">%s</a>: %s</li>' % (escape(doi, True), escape(doi), title))
        ret.append("</ul></p>")
    body = '\n'.join(ret)
    if mode == 'text':
        return ""
    return page(req=req, title=page_title, body=body)


def csv(req):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = 'attachment; filename=scoap3.csv'
    header = ','.join(['Nation'] + [get_coll_i18nname(journal) for journal in CFG_JOURNALS])
    print >> req, header
    for nation_tuple in _CFG_NATION_MAP:
        query = _build_query(nation_tuple)
        line = ','.join([nation_tuple[0]] + [str(len(perform_request_search(p=query, cc=journal, of='intbitset'))) for journal in CFG_JOURNALS])
        print >> req, line


def create_search_from_affiliation(aff):
    return '|'.join(t for t in CFG_SELECTED_AFF[aff])


def us_affiliations(req):
    from invenio.search_engine_utils import get_fieldvalues

    req.content_type = "text/html"
    print >> req, pageheaderonly("USA affiliations", req=req)

    affiliations = []
    tmp = []
    tmp.extend(get_fieldvalues(perform_request_search(p="*"), '100__u', False))
    tmp.extend(get_fieldvalues(perform_request_search(p="*"), '100__v', False))
    tmp.extend(get_fieldvalues(perform_request_search(p="*"), '700__u', False))
    tmp.extend(get_fieldvalues(perform_request_search(p="*"), '700__v', False))
    affiliations.extend(filter(lambda x: "United States of America" in x or "United States" in x or "USA" in x or "U.S.A" in x, tmp))
    affiliations = set(affiliations)

    affs = map(lambda x: x.replace('United States of America', '').replace("United States", '').replace("USA", '').replace("U.S.A", '').replace("University", '').replace("State", '').replace('Department of Physics and Astronomy', "").replace('Department of Physics', "").replace('Department', '').replace(",", '').strip(), affiliations)
    affiliations2 = zip(affiliations, affs)

    for a in sorted(affiliations2, key=lambda aff: aff[1]):
        req.write(a[0]+'<br />')
    req.write(pagefooteronly(req=req))
    return ""


def us_affiliations_csv(req):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = 'attachment; filename=us_aff.csv'
    header = ','.join(['University'] + [get_coll_i18nname(journal) for journal in CFG_JOURNALS] + ['sum'])
    print >> req, header
    for university in CFG_SELECTED_AFF:
        line = university
        count = 0
        search = create_search_from_affiliation(university)
        for collection in CFG_JOURNALS:
            res = perform_request_search(p='/%s/' % (search,), c=collection)
            line = line + "," + str(len(res))
            count = count + len(res)
        print >> req, line+","+str(count)


def usa_papers(req):
    req.content_type = "text/html"
    print >> req, pageheaderonly("USA papers for selected affiliations", req=req)

    ## print the list of linkt to the articles
    for university in CFG_SELECTED_AFF:
        print >> req, "<h2>%s</h2>" % (str(university),)
        search = create_search_from_affiliation(university)
        for collection in CFG_JOURNALS:
            res = perform_request_search(p='/%s/' % (search,), c=collection)
            if len(res):
                print >> req, "<h3>%s (%i)</h3>" % (str(collection), len(res))
                print >> req, "<ul>"
                for rec_id in res:
                    rec = get_record(rec_id)
                    line = "<li><a href='https://repo.scoap3.org/record/%s'>%s</a></li>" % (str(rec_id), str(rec['245'][0][0][0][1]))
                    print >> req, line
                print >> req, "</ul>"

    req.write(pagefooteronly(req=req))
    return ""


def usa_papers_csv(req):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = 'attachment; filename=usa_papers.csv'

    ## print the list of linkt to the articles
    for university in CFG_SELECTED_AFF:
        print >> req, university
        search = create_search_from_affiliation(university)
        for collection in CFG_JOURNALS:
            res = perform_request_search(p='(%s)' % (search,), c=collection)
            if len(res):
                print >> req, collection
                for rec_id in res:
                    rec = get_record(rec_id)
                    line = "%s; https://repo.scoap3.org/record/%s" % (str(rec['245'][0][0][0][1]), str(rec_id))
                    print >> req, line
                print >> req, ""
        print >> req, ""
        print >> req, ""
