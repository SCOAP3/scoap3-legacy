from invenio.webinterface_handler_config import HTTP_BAD_REQUEST, SERVER_RETURN
from invenio.webpage import pagefooteronly, pageheaderonly, page
from invenio.config import CFG_SITE_URL
from os.path import join
from cgi import escape
from urllib import urlencode
from time import strftime

from invenio.search_engine import (perform_request_search,
                                   get_creation_date,
                                   get_modification_date,
                                   get_record,
                                   get_collection_reclist)
from invenio.bibdocfile import BibRecDocs


from invenio.rawtext_search import RawTextSearch


JOURNALS_PDFA = {'ELS/NPB': 'nuclphysb', 'ELS/PLB': 'physletb', 'SPR/EPJC': 'epjc', 'SPR/JHEP': 'JHEP02', 'HIN/AHEP': '10.1155', 'OUP/PTEP': 'ptep'}
JOURNALS_NO_PDFA = {'IOP/CPC': '1674-1137', 'IOP/JCAP': '1475-7516', 'IOP/NJP': '1367-2630'}
JOURNALS_NO_XML = {'JAG/ACTA': 'APhysPolB'}

non_compliance_checks = {"cc": RawTextSearch("-('CC-BY' 'CC BY' 'Creative Commons Attribution') /(copyright|c|©)[^.]*(IOP|Institute of Physics)/"),
                         "authors": RawTextSearch("-(/(c|\(c\)|©) the author/ 'copyright cern')"),
                         "scoap3": RawTextSearch("-'funded by SCOAP'")
                         }


def get_latest_pdf(bibrec_latest_files):
    for file in bibrec_latest_files:
        if file.format == '.pdf' or file.format == '.pdf;pdfa':
            return file
    return None


def is_compliant(recid, non_compliance_checks_key):
    bibrec = BibRecDocs(recid)
    bibdoc = get_latest_pdf(bibrec.list_latest_files())
    try:
        rawtext = bibdoc.bibdoc.get_text()
    except:
        return "<b>NO</b>"

    if non_compliance_checks[non_compliance_checks_key].search(rawtext):
        return "<b>NO</b>"
    return "YES"


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


def write_html(dictionary, journal_list, f_date, t_date, created_or_modified_date, return_val):
    for key in journal_list:
        val = dictionary[key]
        papers = perform_request_search(p="date%s:%s->%s 024:'%s'" % (created_or_modified_date, f_date, t_date, val,))

        if papers == []:
            continue

        return_val.append("<h2>%s</h2>" % (key,))
        return_val.append("<table class='compliance'>\n")
        return_val.append("<thead>\n")
        return_val.append("""<tr>
            <th>recid</th>
            <th>cr. date</th>
            <th>mod. date</th>
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
        return_val.append("</thead>\n")
        return_val.append('<tbody>\n')
        for recid in papers:
            rec = get_record(recid)
            doi = get_doi(rec)
            record_compl = is_complete_record(recid)
            return_val.append("""<tr>
                <td><a href="%s">%i</a></td>
                <td>%s</td>
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
                        get_modification_date(recid),
                        doi, doi,
                        has_or_had_format(recid, '.xml'),
                        has_or_had_format(recid, '.pdf'),
                        has_or_had_format(recid, '.pdf;pdfa'),
                        check_complete_rec(record_compl),
                        get_arxiv(rec),
                        is_compliant(recid, "authors"),
                        is_compliant(recid, "cc"),
                        is_compliant(recid, "scoap3"),
                        str([rec_key for rec_key, rec_val in record_compl.iteritems() if not rec_val])))
        return_val.append('</tbody>\n')
        return_val.append("</table>\n")


def prepare_filter_variables(collections, from_date, to_date):
    collections = collections.split()
    if collections == []:
        pdfa_journals = sorted([item for item in JOURNALS_PDFA])
        no_pdfa_journals = sorted([item for item in JOURNALS_NO_PDFA])
        no_xml_journals = sorted([item for item in JOURNALS_NO_XML])
    else:
        pdfa_journals = sorted([item for item in JOURNALS_PDFA for collection in collections if item.lower().find(collection.lower()) != -1])
        no_pdfa_journals = sorted([item for item in JOURNALS_NO_PDFA for collection in collections if item.lower().find(collection.lower()) != -1])
        no_xml_journals = sorted([item for item in JOURNALS_NO_XML for collection in collections if item.lower().find(collection.lower()) != -1])

    if from_date == '':
        from_date = '1970-01-01'
    if to_date == '':
        to_date = strftime("%Y-%m-%d")

    return pdfa_journals, no_pdfa_journals, no_xml_journals, from_date, to_date


def check_compliance_html(req, collections='', from_date='', to_date='', created_or_modified_date=''):
    return_val = []

    pdfa_journals, no_pdfa_journals, no_xml_journals, from_date, to_date = prepare_filter_variables(collections, from_date, to_date)

    write_html(JOURNALS_PDFA, pdfa_journals, from_date, to_date, created_or_modified_date, return_val)
    write_html(JOURNALS_NO_PDFA, no_pdfa_journals, from_date, to_date, created_or_modified_date, return_val)
    write_html(JOURNALS_NO_XML, no_xml_journals, from_date, to_date, created_or_modified_date, return_val)
    return "".join(return_val)


def index(req):
    req.content_type = "text/html"
    req.write(pageheaderonly("Compliance checks", req=req))
    req.write("<h1>Compliance checks:</h1>")

    journal_list_html = ''
    journal_list_html += "<ol id='selectable'>"
    for key in sorted(JOURNALS_PDFA.keys()) + sorted(JOURNALS_NO_PDFA.keys()) + sorted(JOURNALS_NO_XML.keys()):
        journal_list_html += "<li>" + key + "</li>"
    journal_list_html += "</ol>"
    req.write(journal_list_html)

    req.write("<br/>")
    req.write("<br/>")
    req.write("<select id='date_selector'><option>created</option><option>modified</option></select>")
    req.write(" between:")
    req.write("<input type='text' id='datepicker_from'>")
    req.write(" and:")
    req.write("<input type='text' id='datepicker_to'>")
    req.write('''
            <button onclick=\"
                var journals = '';
                $('.ui-selected').each(
                    function(index) {
                        journals += $(this).text() + ' ';
                    }
                );

                $('#content').html('Loading...');

                from_date = $('#datepicker_from').val();
                to_date = $('#datepicker_to').val();

                selected_date = $('#date_selector option:selected').text();

                $.get('/compliance.py/check_compliance_html', {collections:journals, from_date:from_date, to_date:to_date, created_or_modified_date:selected_date}).done(function(data){$('#content').html(data);});

                \">Check Compliance</button>
        ''')

    req.write('''
            <button onclick=\"
                var journals = '';
                $('.ui-selected').each(
                    function(index) {
                        journals += $(this).text() + ' ';
                    }
                );

                from_date = $('#datepicker_from').val();
                to_date = $('#datepicker_to').val();

                selected_date = $('#date_selector option:selected').text();

                var iframe = document.createElement('iframe');
                iframe.src = '/compliance.py/check_compliance_csv?collections=' + journals + '&from_date=' + from_date + '&to_date=' + to_date + '&created_or_modified_date=' + selected_date; 
                iframe.style.display = 'none';
                document.body.appendChild(iframe);

                \">CSV</button>
        ''')

    req.write("<script src='../js/jquery-ui.min.js'></script>")
    req.write('''
        <script>
            $(function() {$(\"#datepicker_from\").datepicker({ dateFormat: 'yy-mm-dd', maxDate: '+0d', changeMonth: true, changeYear: true });});
            $(function() {$(\"#datepicker_to\").datepicker({ dateFormat: 'yy-mm-dd', maxDate: '+0d', changeMonth: true, changeYear: true });});
            $(function() {$(\"#selectable\").selectable();});
            $(function() {$(\"#selectable\").css("list-style-type", "none");});
        </script>''')

    req.write("<div id=\"content\"></div>")
    req.write(pagefooteronly(req=req))
    req.flush()


def write_csv(req, dictionary, journal_list, f_date, t_date, created_or_modified_date):

    return_val = ''

    for key in journal_list:
        val = dictionary[key]
        papers = perform_request_search(p="date%s:%s->%s 024:'%s'" % (created_or_modified_date, f_date, t_date, val,))

        if papers == []:
            continue

        return_val += key
        return_val += ','.join(['recid', 'cr. date', 'mod. date', 'DOI', 'XML', 'PDF', 'PDF/A', 'Complete record?', 'arXiv number', 'Copyright: authors', 'CC-BY', 'Funded by SCOAP3', 'notes']) + '\n'

        for recid in papers:
            rec = get_record(recid)
            doi = get_doi(rec)
            record_compl = is_complete_record(recid)
            return_val += ','.join(str(item) for item in [str(recid),
                                   get_creation_date(recid),
                                   get_modification_date(recid),
                                   doi,
                                   has_or_had_format(recid, '.xml').lstrip('<b>').rstrip('</b>'),
                                   has_or_had_format(recid, '.pdf').lstrip('<b>').rstrip('</b>'),
                                   has_or_had_format(recid, '.pdf;pdfa').lstrip('<b>').rstrip('</b>'),
                                   str(check_complete_rec(record_compl)),
                                   get_arxiv(rec).lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, 'authors').lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, 'cc').lstrip('<b>').rstrip('</b>'),
                                   is_compliant(recid, 'scoap3').lstrip('<b>').rstrip('</b>'),
                                   str([rec_key for rec_key, rec_val in record_compl.iteritems() if not rec_val])])
            return_val += '\n'

    return return_val


def check_compliance_csv(req, collections='', from_date='', to_date='', created_or_modified_date=''):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = 'attachment; filename=scoap3_compliance.csv'

    pdfa_journals, no_pdfa_journals, no_xml_journals, from_date, to_date = prepare_filter_variables(collections, from_date, to_date)

    tmp = write_csv(req, JOURNALS_PDFA, pdfa_journals, from_date, to_date, created_or_modified_date) \
        + write_csv(req, JOURNALS_NO_PDFA, no_pdfa_journals, from_date, to_date, created_or_modified_date) \
        + write_csv(req, JOURNALS_NO_XML, no_xml_journals, from_date, to_date, created_or_modified_date)
    print >> req, tmp
