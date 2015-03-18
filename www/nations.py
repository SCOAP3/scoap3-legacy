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

from cgi import escape
from urllib import urlencode

from invenio.webinterface_handler_config import HTTP_BAD_REQUEST, SERVER_RETURN
from invenio.webpage import pagefooteronly, pageheaderonly, page
from invenio.search_engine import perform_request_search
from invenio.search_engine import (get_coll_i18nname,
                                   get_record,
                                   get_collection_reclist)
from invenio.bibrecord import record_get_field_value
from invenio.dbquery import run_sql
from invenio.utils import NATIONS_DEFAULT_MAP, multi_replace, get_doi
from invenio.bibrecord import record_get_field_values, record_get_field_value

import re

_AFFILIATIONS = (sorted(list(set(NATIONS_DEFAULT_MAP.values())))
                 + ['HUMAN CHECK'])

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

CFG_SELECTED_AFF = {'Andrews University':
                    ('Andrews University',),
                    'Arkansas State University':
                    ('Arkansas State University',),
                    'Black Hills State University':
                    ('Black Hills State University',),
                    'Boise State University':
                    ('Boise State University',),
                    'Brookhaven National Laboratory':
                    ('Brookhaven National Laboratory',),
                    'Brown University':
                    ('Brown University',),
                    'Chicago State University':
                    ('Chicago State University',),
                    'Columbia University':
                    ('Columbia University',),
                    'Creighton University':
                    ('Creighton University',),
                    'Fairfield University':
                    ('Fairfield University',),
                    'George Washington University':
                    ('George Washington University',),
                    'Hampton University':
                    ('Hampton University',),
                    'Houston Advanced Research Center':
                    ('Houston Advanced Research Center',),
                    'Janelia Farm Research Campus':
                    ('Janelia Farm Research Campus',),
                    'Long Island University':
                    ('Long Island University',),
                    'Louisiana Tech University':
                    ('Louisiana Tech University',),
                    'Luther College':
                    ('Luther College',),
                    'Manhattan College':
                    ('Manhattan College',),
                    'Milwaukee School of Engineering':
                    ('Milwaukee School of Engineering',),
                    'Mississippi State University':
                    ('Mississippi State University',),
                    'Muhlenberg College':
                    ('Muhlenberg College',),
                    'New York City College of Technology':
                    ('New York City College of Technology',),
                    'North Carolina Central University':
                    ('North Carolina Central University',),
                    'Northern Illinois University':
                    ('Northern Illinois University',),
                    'Oklahoma State University':
                    ('Oklahoma State University',),
                    'Pacific Lutheran University':
                    ('Pacific Lutheran University',),
                    'Philander Smith College':
                    ('Philander Smith College',),
                    'Rutgers University':
                    ('Rutgers University',),
                    'South Dakota School of Mines and Technology':
                    ('South Dakota School of Mines and Tec',),
                    'Stanford University':
                    ('Stanford University',),
                    'State University of New York (or SUNY) Albany':
                    ('SUNY Albany', 'University at Albany (SUNY)', 'Albany'),
                    'State University of New York (or SUNY) Buffalo':
                    ('University at Buffalo',
                     'State University of New York at Buffalo'),
                    'Syracuse University':
                    ('Syracuse University',),
                    'Tennessee Tech University':
                    ('Tennessee Tech University',),
                    'Texas Tech University':
                    ('Texas Tech University',),
                    'The George Washington University':
                    ('The George Washington University',),
                    ('The Graduate School and University Center, '
                     'The City University of New York'):
                    (('The Graduate School and University Center, '
                      'The City University o'),),
                    'The Rockefeller University':
                    ('The Rockefeller University',),
                    'The University of Alabama, Tuscaloosa':
                    ('The University of Alabama, Tuscaloosa',),
                    'The University of Mississippi':
                    ('The University of Mississippi',),
                    'Triangle Universities Nuclear Laboratory':
                    ('Triangle Universities Nuclear Laboratory',),
                    'University of Connecticut':
                    ('University of Connecticut',),
                    'University of Hawaii':
                    ('University of Hawaii',),
                    'University of Houston':
                    ('University of Houston',),
                    'University of Puerto Rico':
                    ('University of Puerto Rico',),
                    'University of South Dakota':
                    ('University of South Dakota',),
                    'Utah Valley University':
                    ('Utah Valley University',),
                    'Virginia Military Institute':
                    ('Virginia Military Institute',),
                    'Wayne State University':
                    ('Wayne State University',),
                    'Wayne University':
                    ('Wayne State university',),
                    'Western Michigan University':
                    ('Western Michigan University',),
                    'Yale University': ('Yale University',)}


def _build_query(nation):
    return "100__w:'{0}' OR 700__w:'{0}'".format(nation)


def index(req):
    req.content_type = "text/html"
    req.write(pageheaderonly("Nation numbers", req=req))
    req.write("<h1>Nation numbers</h1>")
    req.flush()
    req.write("<table>\n")

    tr = ("<tr>"
          "<td>{0}</td>"
          "<td><a href='/search?{1}&sc=1'>{2}</a></td>"
          "<td><a href='/nations.py/articles?i={3}' "
          "target='_blank'>Articles</a> "
          "(<a href='/nations.py/articles?mode=text&amp;i={3}'>text</a>)"
          "</td><tr>\n")

    for i, nation in enumerate(_AFFILIATIONS):
        query = _build_query(nation)
        results = perform_request_search(p=query, of='intbitset')
        req.write(tr.format(escape(nation),
                            escape(urlencode([("p", query)]), True),
                            len(results),
                            i))
        req.flush()
    req.write("</table>\n")
    req.write(pagefooteronly(req=req))
    return ""


def late(req):
    req.content_type = "text/html"
    print >> req, pageheaderonly("Late journals", req=req)

    th = ("<tr><th>DOI</th><th>Title</th><th>DOI registration</th>"
          "<th>Arrival in SCOAP3</th></tr>")
    tr = ("<tr style='background-color: {0};'><td>"
          "<a href='http://dx.doi.org/{1}' target='_blank'>{2}</td>"
          "<td>{3}</td><td>{4}</td><td>{5}</td></tr>")

    sql_bibrec = "SELECT creation_date FROM bibrec WHERE id=%s"
    sql_doi = "SELECT creation_date FROM doi WHERE doi=%s"

    for journal in CFG_JOURNALS:
        print >> req, "<h2>%s</h2>" % escape(get_coll_i18nname(journal))
        results = get_collection_reclist(journal)
        print >> req, "<table>"
        print >> req, th
        for recid in results:
            creation_date = run_sql(sql_bibrec, (recid, ))[0][0]
            record = get_record(recid)
            doi = record_get_field_value(record, '024', '7', code='a')
            title = record_get_field_value(record, '245', code='a')
            doi_date = run_sql(sql_doi, (doi, ))
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
            print >> req, tr.format(background,
                                    escape(doi, True),
                                    escape(doi),
                                    title,
                                    doi_date,
                                    creation_date)
        print >> req, "</table>"


def articles(req, i, mode='html'):
    try:
        i = int(i)
        assert 0 <= i < len(_AFFILIATIONS)
    except:
        raise SERVER_RETURN(HTTP_BAD_REQUEST)
    nation = _AFFILIATIONS[i]
    ret = []
    page_title = "SCOAP3 Articles by authors from %s" % nation
    if mode == 'text':
        req.content_type = "text/plain; charset=utf8"
        req.headers_out['content-disposition'] = ('attachment; filename=%s.txt'
                                                  % nation)
    else:
        req.content_type = "text/html"
    if mode == 'text':
        print >> req, page_title
        print >> req, "-" * len(page_title)
    query = _build_query(nation)
    for journal in CFG_JOURNALS:
        results = perform_request_search(p=query, cc=journal, of='intbitset')
        if not results:
            continue
        ret.append("<h2>%s (%s)</h2" % (escape(get_coll_i18nname(journal)),
                                        len(results)))
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

            li = ("<li><a href='http://dx.doi.org/{0}' "
                  "target='_blank'>{1}</a>: {2}</li>")
            ret.append(li.format(escape(doi, True), escape(doi), title))
        ret.append("</ul></p>")
    body = '\n'.join(ret)
    if mode == 'text':
        return ""
    return page(req=req, title=page_title, body=body)


def csv(req):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = 'attachment; filename=scoap3.csv'
    header = (','.join(['Nation']
              + [get_coll_i18nname(journal) for journal in CFG_JOURNALS]))
    print >> req, header
    for nation in _AFFILIATIONS:
        query = _build_query(nation)
        line = (','.join([nation]
                + [str(len(perform_request_search(p=query,
                                                  cc=journal,
                                                  of='intbitset')))
                   for journal in CFG_JOURNALS]))
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

    def _find_usa(x):
        return ("United States of America" in x
                or "United States" in x
                or "USA" in x
                or "U.S.A" in x)
    affiliations.extend(filter(_find_usa, tmp))
    affiliations = set(affiliations)

    replaces = [('United States of America', ''),
                ("United States", ''),
                ("USA", ''),
                ("U.S.A", ''),
                ("University", ''),
                ("State", ''),
                ('Department of Physics and Astronomy', ""),
                ('Department of Physics', ""),
                ('Department', ''),
                (",", '')]

    affs = map(lambda x: multi_replace(x, replaces).strip(), affiliations)
    affiliations2 = zip(affiliations, affs)

    for a in sorted(affiliations2, key=lambda aff: aff[1]):
        req.write(a[0]+'<br />')
    req.write(pagefooteronly(req=req))
    return ""


def us_affiliations_csv(req):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = 'attachment; filename=us_aff.csv'
    header = (';'.join(['University']
              + [get_coll_i18nname(journal) for journal in CFG_JOURNALS]
              + ['sum']))
    print >> req, header
    for university in sorted(CFG_SELECTED_AFF):
        line = university
        count = 0
        search = create_search_from_affiliation(university)
        for collection in CFG_JOURNALS:
            res = perform_request_search(p='/%s/' % (search,), c=collection)
            line = line + ";" + str(len(res))
            count = count + len(res)
        print >> req, line+";"+str(count)


def usa_papers(req):
    req.content_type = "text/html"
    print >> req, pageheaderonly("USA papers for selected affiliations",
                                 req=req)

    li = "<li><a href='https://repo.scoap3.org/record/{0}'>{1}</a></li>"

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
                    line = li.format(str(rec_id), str(rec['245'][0][0][0][1]))
                    print >> req, line
                print >> req, "</ul>"

    req.write(pagefooteronly(req=req))
    return ""


def usa_papers_csv(req):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = ('attachment; '
                                              'filename=usa_papers.csv')

    li = "%s; https://repo.scoap3.org/record/%s"

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
                    line = li.format(str(rec['245'][0][0][0][1]), str(rec_id))
                    print >> req, line
                print >> req, ""
        print >> req, ""
        print >> req, ""


def papers_by_country_csv(req, country):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = ('attachment; '
                                              'filename=papers_by_country.csv')

    ## print the list of linkt to the articles
    count = 1
    print >> req, country
    search = "100__w:'%s' OR 700__w:'%s'" % (country, country)
    res = perform_request_search(p='%s' % (search,))
    print >> req, "#;Title;Author;Journal;DOI;Inspire record"
    if len(res):
        for rec_id in res:
            author_count = 11
            rec = get_record(rec_id)
            title = ''
            authors = ''
            journal = ''
            doi = ''
            inspire_record = ''
            if '245' in rec:
                title = re.sub("<.*?>", "", rec['245'][0][0][0][1])
            if '100' in rec:
                authors = rec['100'][0][0][0][1]
            if '700' in rec:
                for auth in rec['700']:
                    if author_count > 1:
                        authors += " / %s" % (auth[0][0][1],)
                        author_count -= 1
                    elif author_count == 1:
                        authors += " / et al"
                        author_count -= 1
                    else:
                        break
            for sub in rec['773'][0][0]:
                if 'p' in sub[0]:
                    journal = sub[1]
            doi = get_doi(rec_id)
            if '035' in rec:
                for f in rec['035'][0][0]:
                    if 'a' in f:
                        inspire_record = 'http://inspirehep.net/record/%s' % (f[1],)
            print >> req, "%s;%s;%s;%s;%s;%s" % (count, title, authors, journal, doi, inspire_record)
            count += 1


def countries_by_publishers(req):
    req.content_type = "text/html"
    print >> req, pageheaderonly("Countries/publishers", req=req)

    journals = []
    for pub in CFG_JOURNALS:
        ids = perform_request_search(cc=pub)
        journals.append((pub, ids))
    journals.append(("older_than_2014", perform_request_search(cc='older_than_2014')))

    countries = []
    for country in sorted(set(NATIONS_DEFAULT_MAP.itervalues())):
        ids = perform_request_search(p="country:%s" % (country,)) + perform_request_search(cc='older_than_2014', p="country:%s" % (country,))
        countries.append((country, ids))

    req.write("<h1>Number of articles per country per journal</h1>")
    req.flush()
    req.write("<table>\n")
    req.write("<tr><th rowspan=2>Country</th><th colspan=10>Journals</th><th>Other</th></tr>")
    req.write("""<tr>
<td>Acta</td>
<td>Advances in High Energy Physics</td>
<td>Chinese Physics C</td>
<td>European Physical Journal C</td>
<td>Journal of Cosmology and Astroparticle Physics</td>
<td>Journal of High Energy Physics</td>
<td>New Journal of Physics</td>
<td>Nuclear Physics B</td>
<td>Physics Letters B</td>
<td>Progress of Theoretical and Experimental Physics</td>
<td>older_than_2014</td></tr>""")

    for country, c_value in countries:
        req.write("<tr><td>%s</td>" % (country,))
        for journal, j_value in journals:
            req.write("<td>%s</td>" % (len(set(c_value) & set(j_value)),))
        req.write("</tr>")

    req.write('</table>')
    req.write(pagefooteronly(req=req))
    return ""


def impact_articles(req, year):
    try:
        year = int(year)
        assert 2014 <= year
    except:
        raise SERVER_RETURN(HTTP_BAD_REQUEST)

    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = ('attachment; '
                                              'filename=impact_articles.csv')

    ids = perform_request_search(p="datecreated:{year}-01-01->{year}-12-31".format(year=year))
    counter = 0
    print >> req, "#;recid;journal;author;orcid;affiliation;countries"
    for i in ids:
        counter += 1
        try:
            rec = get_record(i)
        except:
            print >> req, "{c},{recid},Can't load metadata".format(c=counter, recid=i)
            continue
        journal = record_get_field_value(rec, tag='773', code='p')
        for field in ['100', '700']:
            if field in rec:
                for author in rec[field]:
                    name = ""
                    orcid = ""
                    aff = ""
                    country = ""
                    for key, val in author[0]:
                        if key is 'a':
                            name = unicode(val, 'UTF-8').replace('\n', ' ').strip()
                        if key is 'j':
                            orcid = unicode(val, 'UTF-8').replace('\n', ' ').strip()
                        if key in ['v', 'u']:
                            aff += unicode(val, 'UTF-8').replace('\n', ' ').strip() + " | "
                        if key is 'w':
                            country += unicode(val, 'UTF-8').replace('\n', ' ').strip() + ";"
                    print >> req, "{c};{recid};{journal};{name};{orcid};{aff};{country}".format(c=counter, recid=i, journal=journal, name=name, orcid=orcid, aff=aff, country=country)
