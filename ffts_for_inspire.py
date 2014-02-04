from invenio.webinterface_handler_config import HTTP_BAD_REQUEST, SERVER_RETURN
from invenio.webpage import pagefooteronly, pageheaderonly, page
from cgi import escape

from invenio.search_engine import search_pattern
from invenio.search_engine import get_creation_date
from invenio.search_engine import get_record
from invenio.bibdocfile import BibRecDocs


def get_list():
    papers = []
    prev_version = search_pattern(p='037:arXiv')

    for recid in prev_version:
        rec = get_record(recid)
        if '037' in rec.keys():
            if ('9', 'arXiv') in rec.get('037')[0][0]:
                for t in rec.get('037')[0][0]:
                    if 'a' in t:
                        url = ""
                        for f in BibRecDocs(recid).get_bibdoc('main').list_latest_files():
                            if f.format in ('.pdf', '.pdf;pdfa'):
                                if url:
                                    if f.format is ".pdf;pdfa":
                                        url = f.url
                                else:
                                    url = f.url
                        papers.append((recid, t[1], get_creation_date(recid), url))
    return papers


def index(req):
    req.content_type = "text/html"
    req.write(pageheaderonly("Papers with arXiv number", req=req))
    req.write("<h1>Papers with arXiv numbers:</h1>")
    req.flush()
    req.write("<table>\n")

    papers = get_list()
    for i, paper_tuple in enumerate(papers):
        req.write("""<tr><td>%i</td><td>%i</td><td>%s</td><td>%s</td>""" % (i, paper_tuple[0], paper_tuple[1], paper_tuple[2]))
        if paper_tuple[3]:
            req.write("""<td><a href='%s'>link</a></td></tr>\n""" % (paper_tuple[3], ))
        else:
            req.write("""<td>no pdf</td></tr>\n""")
        req.flush()
    req.write("</table>\n")
    req.write(pagefooteronly(req=req))
    return ""

# def late(req):
#     req.content_type = "text/html"
#     print >> req, pageheaderonly("Late journals", req=req)
#     for journal in CFG_JOURNALS:
#         print >> req, "<h2>%s</h2>" % escape(get_coll_i18nname(journal))
#         results = get_collection_reclist(journal)
#         print >> req, "<table>"
#         print >> req, "<tr><th>DOI</th><th>Title</th><th>DOI registration</th><th>Arrival in SCOAP3</th></tr>"
#         for recid in results:
#             creation_date = run_sql("SELECT creation_date FROM bibrec WHERE id=%s", (recid, ))[0][0]
#             record = get_record(recid)
#             doi = record_get_field_value(record, '024', '7', code='a')
#             title = record_get_field_value(record, '245', code='a')
#             doi_date = run_sql("SELECT creation_date FROM doi WHERE doi=%s", (doi, ))
#             background = "#eee"
#             if doi_date:
#                 doi_date = doi_date[0][0]
#                 if (creation_date - doi_date).days < 0:
#                     background = "#66FF00"
#                 elif (creation_date - doi_date).days < 1:
#                     background = "#FF6600"
#                 else:
#                     background = "#FF0000"
#             else:
#                 doi_date = ''
#             print >> req, '<tr style="background-color: %s;"><td><a href="http://dx.doi.org/%s" target="_blank">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
#                     background,
#                     escape(doi, True),
#                     escape(doi),
#                     title,
#                     doi_date,
#                     creation_date)
#         print >> req, "</table>"

# def articles(req, i, mode='html'):
#     try:
#         i = int(i)
#         assert 0 <= i < len(_CFG_NATION_MAP)
#     except:
#         raise SERVER_RETURN(HTTP_BAD_REQUEST)
#     nation_tuple = _CFG_NATION_MAP[i]
#     ret = []
#     page_title = "SCOAP3 Articles by authors from %s" % nation_tuple[0]
#     if mode == 'text':
#         req.content_type = "text/plain; charset=utf8"
#         req.headers_out['content-disposition'] = 'attachment; filename=%s.txt' % nation_tuple[0]
#     else:
#         req.content_type = "text/html"
#     if mode == 'text':
#         print >> req, page_title
#         print >> req, "-" * len(page_title)
#     query = _build_query(nation_tuple)
#     for journal in CFG_JOURNALS:
#         results = perform_request_search(p=query, cc=journal, of='intbitset')
#         if not results:
#             #ret.append("<p>No articles yet</p>")
#             continue
#         ret.append("<h2>%s (%s)</h2" % (escape(get_coll_i18nname(journal)), len(results)))
#         ret.append("<p><ul>")
#         if mode == 'text':
#             print >> req, ""
#             print >> req, get_coll_i18nname(journal)
#         for recid in results:
#             record = get_record(recid)
#             title = record_get_field_value(record, '245', code='a')
#             doi = record_get_field_value(record, '024', '7', code='a')
#             if mode == 'text':
#                 print >> req, "http://dx.doi.org/%s" % doi
#             ret.append('<li><a href="http://dx.doi.org/%s" target="_blank">%s</a>: %s</li>' % (escape(doi, True), escape(doi), title))
#         ret.append("</ul></p>")
#     body = '\n'.join(ret)
#     if mode == 'text':
#         return ""
#     return page(req=req, title=page_title, body=body)

# def csv(req):
#     req.content_type = 'text/csv; charset=utf-8'
#     req.headers_out['content-disposition'] = 'attachment; filename=scoap3.csv'
#     header = ','.join(['Nation'] + [get_coll_i18nname(journal) for journal in CFG_JOURNALS])
#     print >> req, header
#     for nation_tuple in _CFG_NATION_MAP:
#         query = _build_query(nation_tuple)
#         line = ','.join([nation_tuple[0]] + [str(len(perform_request_search(p=query, cc=journal, of='intbitset'))) for journal in CFG_JOURNALS])
#         print >> req, line
