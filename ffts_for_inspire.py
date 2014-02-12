from invenio.webinterface_handler_config import HTTP_BAD_REQUEST, SERVER_RETURN
from invenio.webpage import pagefooteronly, pageheaderonly, page
from cgi import escape
from urllib import urlencode

from invenio.search_engine import perform_request_search
from invenio.search_engine import get_creation_date
from invenio.search_engine import get_record
from invenio.bibdocfile import BibRecDocs

def get_pdf(recid):
    url = ""
    url_type = ""
    doc = BibRecDocs(recid)
    names = doc.get_bibdoc_names()
    files = []
    checksum = None
    if 'main' in names:
        files = doc.get_bibdoc('main').list_latest_files()
    elif 'fulltext' in names:
        files = doc.get_bibdoc('fulltext').list_latest_files()
    for f in files:
        if f.format in ('.pdf', '.pdf;pdfa'):
            if f.format == ".pdf;pdfa":
                url = f.url
                url_type = ".pdf;pdfa"
            else:
                url = f.url
                url_type = ".pdf"
        if url:
            checksum = f.checksum

    return checksum, url, url_type

def get_list():
    papers = []
    prev_version = perform_request_search()

    for recid in prev_version:
        rec = get_record(recid)
        doi = None
        arxiv_id = None
        try:
            if ('2', 'DOI') in rec['024'][0][0]:
                for t in rec['024'][0][0]:
                    if 'a' in t:
                        doi = t[1]
                if not doi:
                    print "No DOI for record: %i" % (recid, )
            else:
                print "No DOI for record: %i" % (recid, )
        except:
            print "No DOI for record: %i" % (recid, )

        checksum, url, url_type = get_pdf(recid)

        if '037' in rec.keys():
            if ('9', 'arXiv') in rec.get('037')[0][0]:
                for t in rec.get('037')[0][0]:
                    if 'a' in t:
                        arxiv_id = t[1]

        papers.append((recid, arxiv_id, get_creation_date(recid), checksum, url, url_type, doi))
    return papers


def index(req):
    req.content_type = "text/html"
    req.write(pageheaderonly("Papers with arXiv number", req=req))
    req.write("<h1>Papers with arXiv numbers:</h1>")
    req.flush()
    req.write("<table>\n")

    papers = get_list()
    for i, paper_tuple in enumerate(papers):
        req.write("""<tr><td>%i</td><td>%i</td><td>%s</td><td>%s</td><td>%s</td>""" % (i, paper_tuple[0], paper_tuple[1], paper_tuple[2], paper_tuple[3]))
        if paper_tuple[3]:
            req.write("""<td><a href='%s'>link</a></td>""" % (paper_tuple[4], ))
        else:
            req.write("""<td>no pdf</td>""")
        req.write("""<td>%s</td>""" % (paper_tuple[5], ))
        req.write("""<td>%s</td></tr>\n""" % (paper_tuple[6], ))
        req.flush()
    req.write("</table>\n")
    req.write(pagefooteronly(req=req))
    return ""


def csv(req):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = 'attachment; filename=scoap3.csv'
    header = ','.join(('recid', 'arxiv_id', 'cr_date', 'checksum', 'link', 'type', 'doi'))
    print >> req, header
    papers = get_list()
    for paper_tuple in papers:
        line = '%i, %s, %s, %s, %s, %s, %s' % paper_tuple
        print >> req, line
