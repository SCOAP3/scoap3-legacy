from invenio.webinterface_handler_config import HTTP_BAD_REQUEST, SERVER_RETURN
from invenio.webpage import pagefooteronly, pageheaderonly, page
from invenio.config import CFG_SITE_URL
from os.path import join
from cgi import escape
from urllib import urlencode

from invenio.search_engine import (perform_request_search,
                                   get_creation_date,
                                   get_record)
from invenio.bibdocfile import BibRecDocs


JOURNALS_PDFA = {'ELS/NPB': 'nuclphysb', 'ELS/PLB': 'physletb', 'SPR/EPJC': 'epjc', 'SPR/JHEP': 'JHEP02', 'HIN/AHEP': '10.1155', 'OUP/PTEP': 'ptep'}
JOURNALS_NO_PDFA = {'IOP/CPC': '1674-1137', 'IOP/JCAP': '1475-7516', 'IOP/NJP': '1367-2630'}
JOURNALS_NO_XML = {'JAG/ACTA': 'APhysPolB'}

no_cc_by = perform_request_search(p="-'CC-BY' -'CC BY' -'Creative Commons Attribution'", f="fulltext")  # looks for papers without "cc-by" string
no_the_authors = perform_request_search(p="-'© the author' -'copyright cern'", f="fulltext")  # looks for papers without "the authors string
no_scoap3 = perform_request_search(p="-'funded by SCOAP'", f="fulltext")  # looks for papers without "the authors string


def get_doi(rec):
    doi = None
    try:
        if ('2', 'DOI') in rec['024'][0][0]:
            for t in rec['024'][0][0]:
                if 'a' in t:
                    doi = t[1]
    except:
        pass
    return doi


def get_arxiv(rec):
    nr = "<b>NO</b>"
    if '037' in rec.keys():
            if ('9', 'arXiv') in rec.get('037')[0][0]:
                for t in rec.get('037')[0][0]:
                    if 'a' in t:
                        nr = t[1]
    return nr


# If the recid is on the list then it means that paper is not compliant.
def is_compliant(recid, filtered_list):
    if recid in filtered_list:
        return "<b>NO</b>"
    else:
        return "yes"


def get_formats(recid):
    doc = BibRecDocs(recid)
    formats = []
    for d in doc.list_latest_files():
        formats.append(d.format)
    return formats


def has_or_had_format(recid, format):
    doc = BibRecDocs(recid)
    formats = []
    ret = 0
    for d in doc.list_latest_files():
        formats.append(d.format)

    if format in formats:
        ret = 1
    else:
        for d in doc.list_bibdocs():
            for dd in d.docfiles:
                if format == dd.format:
                    ret = 2

    if ret == 0:
        return "<b>NO</b>"
    elif ret == 1:
        return "yes"
    elif ret == 2:
        return "<b>diff. v.</b>"


def get_year(rec):
    ret = False
    if '773' in rec:
        for f in rec['773'][0][0]:
            if 'y' in f:
                if f[1]:
                    ret = True
    return ret


def check_authors(rec):
    if '100' in rec:
        for author in rec['100']:
            fields = [f[0] for f in author[0]]
            if 'v' not in fields and 'u' not in fields:
                return False
    else:
        print "no author in %s" % (rec['001'],)
        return False

    if '700' in rec:
        for author in rec['700']:
            fields = [f[0] for f in author[0]]
            if 'v' not in fields and 'u' not in fields:
                return False
        return True
    return True


def is_complete_record(recid):  # no ORCIDs
    rec = get_record(recid)
    title = '245' in rec
    journal_abrev = True  # wtf?
    doi = get_doi(rec)  # ok also for url
    issn = False  # never extracted
    year = get_year(rec)
    authors = check_authors(rec)

    return {'title': title,
            'journal_abrev': journal_abrev,
            'doi': doi,
            'issn': issn,
            'year': year,
            'authors': authors}

def check_complete_rec(dict_with_vals):
    for val in dict_with_vals.itervalues():
        if not val:
            return False
    return True


def index(req):
    req.content_type = "text/html"
    req.write(pageheaderonly("Compliance checks", req=req))
    req.write("<h1>Compliance checks:</h1>")
    req.flush()

    ### all checks
    for key, val in JOURNALS_PDFA.iteritems():
        papers = perform_request_search(p="024:'%s'" % (val,))

        req.write("<h2>%s</h2>" % (key,))
        req.write("<table class='compliance'>\n")
        req.write("<thead>\n")
        req.write("""<tr>
            <th></th>
            <th></th>
            <th></th>
            <th colspan='3'>Format</th>
            <th colspan='2'>Metadata</th>
            <th colspan='3'>Legal: This information should be clearly marked in the PDF</th>
            <th></th>
        </tr>""")
        req.write("""<tr>
            <th>recid</th>
            <th>cr. date</th>
            <th>DOI</th>
            <th>XML</th>
            <th>PDF</th>
            <th>PDF/A</th>
            <th>Complete record?</th>
            <th>arXiv number</th>
            <th>Copyright: authors</th>
            <th>CC-BY</th>
            <th>Funded by SCOAP3</th>
            <th>notes</th>
        </tr>""")
        req.write("</thead>\n")
        req.write('<tbody>\n')
        for recid in papers:
            rec = get_record(recid)
            doi = get_doi(rec)
            record_compl = is_complete_record(recid)
            req.write("""<tr>
                <td><a href="%s">%i</a></td>
                <td>%s</td>
                <td><a href="http://dx.doi.org/%s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>""" % (join(CFG_SITE_URL, 'record', str(recid)), recid,
                        get_creation_date(recid),
                        doi, doi,
                        has_or_had_format(recid, '.xml'),
                        has_or_had_format(recid, '.pdf'),
                        has_or_had_format(recid, '.pdf;pdfa'),
                        check_complete_rec(record_compl),
                        get_arxiv(rec),
                        is_compliant(recid, no_the_authors),
                        is_compliant(recid, no_cc_by),
                        is_compliant(recid, no_scoap3),
                        str([rec_key for rec_key, rec_val in record_compl.iteritems() if not rec_val])))
        req.write('</tbody>\n')
        req.write("</table>\n")

    ### no_pdfa
    for key, val in JOURNALS_NO_PDFA.iteritems():
        papers = perform_request_search(p="024:'%s'" % (val,))

        req.write("<h2>%s</h2>" % (key,))
        req.write("<table class='compliance'>\n")
        req.write("<thead>\n")
        req.write("""<tr>
            <th></th>
            <th></th>
            <th></th>
            <th colspan='2'>Format</th>
            <th colspan='2'>Metadata</th>
            <th colspan='3'>Legal: This information should be clearly marked in the PDF</th>
        </tr>""")
        req.write("""<tr>
            <th>recid</th>
            <th>cr. date</th>
            <th>DOI</th>
            <th>XML</th>
            <th>PDF</th>
            <th>Complete record?</th>
            <th>arXiv number</th>
            <th>Copyright: authors</th>
            <th>CC-BY</th>
            <th>Funded by SCOAP3</th>
        </tr>""")
        req.write("</thead>\n")
        req.write('<tbody>\n')
        for recid in papers:
            rec = get_record(recid)
            doi = get_doi(rec)
            record_compl = is_complete_record(recid)
            req.write("""<tr>
                <td><a href="%s">%i</a></td>
                <td>%s</td>
                <td><a href="http://dx.doi.org/%s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>""" % (join(CFG_SITE_URL, 'record', str(recid)), recid,
                        get_creation_date(recid),
                        doi, doi,
                        has_or_had_format(recid, '.xml'),
                        has_or_had_format(recid, '.pdf'),
                        check_complete_rec(record_compl),
                        get_arxiv(rec),
                        is_compliant(recid, no_the_authors),
                        is_compliant(recid, no_cc_by),
                        is_compliant(recid, no_scoap3),
                        str([rec_key for rec_key, rec_val in record_compl.iteritems() if not rec_val])))
        req.write('</tbody>\n')
        req.write("</table>\n")

    ### no_xml
    for key, val in JOURNALS_NO_XML.iteritems():
        papers = perform_request_search(p="024:'%s'" % (val,))

        req.write("<h2>%s</h2>" % (key,))
        req.write("<table class='compliance'>\n")
        req.write("<thead>\n")
        req.write("""<tr>
            <th></th>
            <th></th>
            <th></th>
            <th colspan='2'>Format</th>
            <th colspan='2'>Metadata</th>
            <th colspan='3'>Legal: This information should be clearly marked in the PDF</th>
        </tr>""")
        req.write("""<tr>
            <th>recid</th>
            <th>cr. date</th>
            <th>DOI</th>
            <th>PDF</th>
            <th>PDF/A</th>
            <th>Complete record?</th>
            <th>arXiv number</th>
            <th>Copyright: authors</th>
            <th>CC-BY</th>
            <th>Funded by SCOAP3</th>
        </tr>""")
        req.write("</thead>\n")
        req.write('<tbody>\n')
        for recid in papers:
            rec = get_record(recid)
            doi = get_doi(rec)
            record_compl = is_complete_record(recid)
            req.write("""<tr>
                <td><a href="%s">%i</a></td>
                <td>%s</td>
                <td><a href="http://dx.doi.org/%s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>""" % (join(CFG_SITE_URL, 'record', str(recid)), recid,
                        get_creation_date(recid),
                        doi, doi,
                        has_or_had_format(recid, '.pdf'),
                        has_or_had_format(recid, '.pdf;pdfa'),
                        check_complete_rec(record_compl),
                        get_arxiv(rec),
                        is_compliant(recid, no_the_authors),
                        is_compliant(recid, no_cc_by),
                        is_compliant(recid, no_scoap3),
                        str([rec_key for rec_key, rec_val in record_compl.iteritems() if not rec_val])))
        req.write('</tbody>\n')
        req.write("</table>\n")

    req.write(pagefooteronly(req=req))
    return ""


def csv(req):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = 'attachment; filename=scoap3_compliance.csv'

    ### all checks
    for key, val in JOURNALS_PDFA.iteritems():
        papers = perform_request_search(p="024:'%s'" % (val,))
        print >> req, key
        print >> req, ','.join(['recid', 'cr. date', 'DOI', 'XML', 'PDF', 'PDF/A', 'Complete record?', 'arXiv number', 'Copyright: authors', 'CC-BY', 'Funded by SCOAP3', 'notes'])

        for recid in papers:
            rec = get_record(recid)
            doi = get_doi(rec)
            record_compl = is_complete_record(recid)
            print >> req, ','.join([str(recid),
                                   get_creation_date(recid),
                                   doi,
                                   has_or_had_format(recid, '.xml').lstrip('<b>').rstrip('</b>'),
                                   has_or_had_format(recid, '.pdf').lstrip('<b>').rstrip('</b>'),
                                   has_or_had_format(recid, '.pdf;pdfa').lstrip('<b>').rstrip('</b>'),
                                   str(check_complete_rec(record_compl)),
                                   get_arxiv(rec).lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, no_the_authors).lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, no_cc_by).lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, no_scoap3).lstrip('<b>').rstrip('</b>'),
                                   str([rec_key for rec_key, rec_val in record_compl.iteritems() if not rec_val])])

    ### no_pdfa
    for key, val in JOURNALS_NO_PDFA.iteritems():
        papers = perform_request_search(p="024:'%s'" % (val,))

        print >> req, key
        print >> req, ','.join(['recid', 'cr. date', 'DOI', 'XML', 'PDF', 'Complete record?', 'arXiv number', 'Copyright: authors', 'CC-BY', 'Funded by SCOAP3', 'notes'])
        for recid in papers:
            rec = get_record(recid)
            doi = get_doi(rec)
            record_compl = is_complete_record(recid)
            print >> req, ','.join([str(recid),
                                   get_creation_date(recid),
                                   doi,
                                   has_or_had_format(recid, '.xml').lstrip('<b>').rstrip('</b>'),
                                   has_or_had_format(recid, '.pdf').lstrip('<b>').rstrip('</b>'),
                                   str(check_complete_rec(record_compl)),
                                   get_arxiv(rec).lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, no_the_authors).lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, no_cc_by).lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, no_scoap3).lstrip('<b>').rstrip('</b>'),
                                   str([rec_key for rec_key, rec_val in record_compl.iteritems() if not rec_val])])

    ### no_xml
    for key, val in JOURNALS_NO_XML.iteritems():
        papers = perform_request_search(p="024:'%s'" % (val,))

        print >> req, key
        print >> req, ','.join(['recid', 'cr. date', 'DOI', 'PDF', 'PDF/A', 'Complete record?', 'arXiv number', 'Copyright: authors', 'CC-BY', 'Funded by SCOAP3', 'notes'])
        for recid in papers:
            rec = get_record(recid)
            doi = get_doi(rec)
            record_compl = is_complete_record(recid)

            print >> req, ','.join([str(recid),
                                   get_creation_date(recid),
                                   doi,
                                   has_or_had_format(recid, '.pdf').lstrip('<b>').rstrip('</b>'),
                                   has_or_had_format(recid, '.pdf;pdfa').lstrip('<b>').rstrip('</b>'),
                                   str(check_complete_rec(record_compl)),
                                   get_arxiv(rec).lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, no_the_authors).lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, no_cc_by).lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, no_scoap3).lstrip('<b>').rstrip('</b>'),
                                   str([rec_key for rec_key, rec_val in record_compl.iteritems() if not rec_val])])
