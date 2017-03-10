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

from invenio.config import CFG_SITE_URL
from os.path import join
from time import strftime
from datetime import timedelta, datetime

from invenio.webpage import (pagefooteronly, pageheaderonly)
from invenio.search_engine import (perform_request_search,
                                   get_creation_date,
                                   get_modification_date,
                                   get_record,
                                   get_collection_reclist)
from invenio.bibdocfile import BibRecDocs
from invenio.dbquery import run_sql
from invenio.errorlib import register_exception


JOURNALS_PDFA = {'ELS/NPB': 'Nuclear Physics B',
                 'ELS/PLB': 'Physics Letters B',
                 'SPR/EPJC': 'European Physical Journal C',
                 'SPR/JHEP': 'Journal of High Energy Physics',
                 'HIN/AHEP': 'Advances in High Energy Physics',
                 'OUP/PTEP': 'Progress of Theoretical and Experimental Physics'}
JOURNALS_NO_PDFA = {'IOP/CPC': 'Chinese Physics C',
                    'IOP/JCAP': 'Journal of Cosmology and Astroparticle Physics',
                    'IOP/NJP': 'New Journal of Physics'}
JOURNALS_NO_XML = {'JAG/ACTA': 'Acta'}

compliance_check_values = {}


def get_compliance_values():
    reclist = get_collection_reclist('SCOAP3 Repository')
    for recid in reclist:
        tmpdic = {}
        rec = get_record(recid)
        if '591' in rec:
            for field in rec['591']:
                if field[0]:
                    str_val = field[0][0][1]
                    key = str_val[:str_val.find(':')].lower()
                    val = int(str_val[str_val.find(':') + 1:])
                    tmpdic[key] = val
            compliance_check_values[recid] = tmpdic


get_compliance_values()


def is_compliant(recid, non_compliance_checks_key):
    try:
        if compliance_check_values[recid][non_compliance_checks_key]:
            return "YES"
        else:
            return "<b>NO</b>"
    except:
        return "<b>Not checked yet</b>"


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


def prepare_filter_variables(collections, from_date, to_date):
    collections = collections.split()
    if collections == []:
        pdfa_journals = sorted([item for item in JOURNALS_PDFA])
        no_pdfa_journals = sorted([item for item in JOURNALS_NO_PDFA])
        no_xml_journals = sorted([item for item in JOURNALS_NO_XML])
    else:
        pdfa_journals = sorted([item for item in JOURNALS_PDFA
                                for collection in collections
                                if item.lower().find(collection.lower()) != -1])
        no_pdfa_journals = sorted([item for item in JOURNALS_NO_PDFA
                                   for collection in collections
                                   if item.lower().find(collection.lower()) != -1])
        no_xml_journals = sorted([item for item in JOURNALS_NO_XML
                                  for collection in collections
                                  if item.lower().find(collection.lower()) != -1])

    if from_date == '':
        from_date = '1970-01-01'
    if to_date == '':
        to_date = strftime("%Y-%m-%d")

    return pdfa_journals, no_pdfa_journals, no_xml_journals, from_date, to_date


def get_recids(req, dictionary, journal_list, f_date, t_date,
               created_or_modified_date, result):
    for key in journal_list:
        val = dictionary[key]
        papers = perform_request_search(p="date%s:%s->%s"
                                        % (created_or_modified_date,
                                           f_date, t_date),
                                        c=val)

        if len(papers) != 0:
            result.extend([key])
            result.extend([str(paper) for paper in papers])


def get_recid_list(req, collections='', from_date='', to_date='',
                   created_or_modified_date=''):

    (pdfa_journals,
     no_pdfa_journals,
     no_xml_journals,
     from_date,
     to_date) = prepare_filter_variables(collections, from_date, to_date)

    result = []

    get_recids(req, JOURNALS_PDFA, pdfa_journals, from_date, to_date,
               created_or_modified_date, result)
    get_recids(req, JOURNALS_NO_PDFA, no_pdfa_journals, from_date, to_date,
               created_or_modified_date, result)
    get_recids(req, JOURNALS_NO_XML, no_xml_journals, from_date, to_date,
               created_or_modified_date, result)

    return result


def get_detiled_package_delivery(doi):
    delivery_data = run_sql("SELECT doi.creation_date AS 'doi_reg', doi.publication_date AS 'pub_date', package.name AS 'pkg_name', package.delivery_date AS 'pkg_delivery' FROM doi_package LEFT JOIN doi ON doi_package.doi=doi.doi LEFT JOIN package ON package.id=doi_package.package_id WHERE doi_package.doi=%s ORDER BY package.delivery_date ASC", (doi,), with_dict=True)
    if delivery_data:
        first_del = delivery_data[0]['pkg_delivery']
        first_ab_del = get_delivery_of_firts_ab_package(delivery_data)
        last_mod = delivery_data[-1]['pkg_delivery']
        doi_reg = delivery_data[0]['doi_reg']
        pdfa_del = get_delivery_of_firts_pdfa(delivery_data)
        pub_date = delivery_data[0]['pub_date']
        return (first_del, first_ab_del, last_mod, doi_reg, pdfa_del, pub_date)
    else:
        return None


def get_general_delivery(recid, doi):
    delivery_data = run_sql("select * from doi where doi='%s'" % (doi,))
    if delivery_data:
        first_del = get_creation_date(recid)
        first_ab_del = None
        last_mod = get_modification_date(recid)
        doi_reg = delivery_data[0][1]
        pdfa_del = None
        pub_date = delivery_data[0][2]
        return (first_del, first_ab_del, last_mod, doi_reg, pdfa_del, pub_date)
    else:
        return None


def get_delivery_data(recid, doi):
    first_del = None
    first_ab_del = None
    last_mod = None
    doi_reg = None
    pdfa_del = None
    pub_date = None

    delivery_data = get_detiled_package_delivery(doi)
    if delivery_data:
        return delivery_data[0], delivery_data[1], delivery_data[2], delivery_data[3], delivery_data[4], delivery_data[5]
    else:
        delivery_data = get_general_delivery(recid, doi)
        if delivery_data:
            return delivery_data[0], delivery_data[1], delivery_data[2], delivery_data[3], delivery_data[4], delivery_data[5]

    return first_del, first_ab_del, last_mod, doi_reg, pdfa_del, pub_date


def get_record_checks(req, recids):
    if recids == '':
        return ''

    recids = recids.split(',')
    return_val = []
    for rid in recids:
        try:
            recid = int(rid)
            rec = get_record(recid)
            doi = get_doi(rec)

            first_del, first_ab_del, last_mod, doi_reg, pdfa_del, pub_date = get_delivery_data(recid, doi)

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
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td %s>%s</td>
                <td %s>%s</td>
        <td>%s</td>
                <td %s>%s</td>
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
                        is_compliant(recid, "category"),
                        str([rec_key for rec_key, rec_val
                             in record_compl.iteritems() if not rec_val]),
                        str(first_del),
                        str(first_ab_del),
                        str(last_mod),
                        str(pdfa_del),
                        str(doi_reg),
                        format_24h_delivery(check_24h_delivery(first_del, doi_reg)),
                        check_24h_delivery(first_del, doi_reg),
                        format_24h_delivery(check_24h_delivery(pdfa_del, doi_reg)),
                        check_24h_delivery(pdfa_del, doi_reg),
                        str(pub_date),
                        format_24h_delivery(check_24h_delivery(first_del, pub_date)),
                        check_24h_delivery(first_del, pub_date)))
        except Exception:
            register_exception()
            recid = rid
            return_val.append("""<tr><th colspan="13" align="left">
                               <h2>%s</h2></th></tr>""" % (recid,))
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
                <th>arXiv category</th>
                <th>notes</th>
                <th>First delivery</th>
                <th>First AB delivery</th>
                <th>Last modification</th>
                <th>PDF/A upload</th>
                <th>DOI registration</th>
                <th>Delivery diff</th>
                <th>PDF/A diff</th>
        <th>Publication online</th>
        <th>Pub. online diff</th>
            </tr>""")
    return ''.join(return_val)


def index(req):
    req.content_type = "text/html"
    req.write(pageheaderonly("Compliance checks", req=req))
    req.write("<h1>Compliance checks:</h1>")

    journal_list_html = ''
    journal_list_html += "<ol id='selectable'>"
    for key in (sorted(JOURNALS_PDFA.keys())
                + sorted(JOURNALS_NO_PDFA.keys())
                + sorted(JOURNALS_NO_XML.keys())):
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
    req.write("<select id='loadall'><option>Load on scroll</option><option>Load all</option></select>")
    req.write('''
            <button onclick=\"
                cc_button = $(this);
                cc_button.prop('disabled', true);
                var shall_load_all = $('#loadall option:selected').text() == 'Load all';
                var journals = '';
                $('.ui-selected').each(
                    function(index) {
                        journals += $(this).text() + ' ';
                    }
                );

                var from_date = $('#datepicker_from').val();
                var to_date = $('#datepicker_to').val();

                var selected_date = $('#date_selector option:selected').text();

                var recid_list = new Array();

                $.get('/compliance.py/get_recid_list', {collections:journals, from_date:from_date, to_date:to_date, created_or_modified_date:selected_date}).done(function(data){
                    count = 0;
                    sublists = new Array();
                    $('#content').html('');

                    if(data == '') {
                        cc_button.prop('disabled', false);
                        $('#content').html('No data for your selection.');
                        return;
                    }

                    var tmp = data.split('\\'').join('').split(' ').join('');
                    var reclist = tmp.substring(1, tmp.length - 1).split(',');

                    batchSize = 100;
                    iterations = reclist.length / batchSize;

                    for(var i = 0; i < iterations; i++){
                        sublists.push(reclist.slice(i*batchSize, (i+1)*batchSize));
                    }

                    if(shall_load_all){
                        load_all();
                    } else {
                        fill_window();
                    }
                });

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
            function load_all(){
                $('#loadingfield').html('Loading...');
                if(count >= iterations){
                    $('#loadingfield').html('');
                    cc_button.prop('disabled', false);
                    return;
                }
                recs = sublists[count].join();
                $.get('/compliance.py/get_record_checks', {recids:recs}).done(function(data){
                    $('#content').append(data);
                    count += 1;
                    load_all();
                });
            }
            function fill_window(){
                $('#loadingfield').html('Loading...');
                if($(document).height() > $(window).height() || count == sublists.length){
                    $('#loadingfield').html('');
                    cc_button.prop('disabled', false);
                    return;
                }
                recs = sublists[count].join();
                $.get('/compliance.py/get_record_checks', {recids:recs}).done(function(data){
                    $('#content').append(data);
                    count += 1;
                    fill_window();
                });
            }
            function next(){
                if(count >= iterations){
                    return;
                }
                $('#loadingfield').html('Loading...');
                recs = sublists[count].join();
                $.get('/compliance.py/get_record_checks', {recids:recs}).done(function(data){
                    $('#loadingfield').html('');
                    $('#content').append(data);
                    count += 1;
                });
            }
            sublists = new Array();
            var count = 0;
            var iterations = 0;
            var cc_button;
            $(function() {$(\"#datepicker_from\").datepicker({ dateFormat: 'yy-mm-dd', maxDate: '+0d', changeMonth: true, changeYear: true });});
            $(function() {$(\"#datepicker_to\").datepicker({ dateFormat: 'yy-mm-dd', maxDate: '+0d', changeMonth: true, changeYear: true });});
            $(function() {$(\"#selectable\").selectable();});
            $(function() {$(\"#selectable\").css("list-style-type", "none");});
            $(window).scroll(function(){
                if($(window).scrollTop() == $(document).height() - $(window).height()){
                    next();
                }
            });
        </script>''')

    req.write("<table id=\"content\" class=\"compliance\"></table>")
    req.write("<div id='loadingfield' style='text-align:center; font-weight:bold;'></div>")
    req.write(pagefooteronly(req=req))
    req.flush()


def get_delivery_of_firts_ab_package(data):
    delivery_date = None
    for delivery in data:
        if 'CERNAB' in delivery['pkg_name']:
            delivery_date = delivery['pkg_delivery']
            break
    return delivery_date


def get_delivery_of_firts_pdfa(data):
    delivery_date = None
    for delivery in data:
        if 'vtex' in delivery['pkg_name']:
            delivery_date = delivery['pkg_delivery']
            break
    return delivery_date


def check_24h_delivery(time, doi_reg):
    if type(time) is str:
        time = datetime.strptime(time,'%Y-%m-%d')
    if time and doi_reg:
        return time - doi_reg
    else:
        return None


def format_24h_delivery(data):
    if data:
        if data > timedelta(1):
            return 'style="background-color:red;"'
    return ''


def write_csv(req, dictionary, journal_list, f_date, t_date,
              created_or_modified_date):
    return_val = ''

    for key in journal_list:
        val = dictionary[key]
        papers = perform_request_search(p="date%s:%s->%s"
                                        % (created_or_modified_date,
                                           f_date, t_date),
                                        c=val)

        if papers == []:
            continue

        return_val += key + '\n'
        return_val += ';'.join(['recid', 'cr. date', 'mod. date', 'DOI',
                                'XML', 'PDF', 'PDF/A', 'Complete record?',
                                'arXiv number', 'Copyright: authors', 'CC-BY',
                                'Funded by SCOAP3', 'arXiv category', 'notes',
                                'First delivery', 'First AB delivery',
                                'Last modification', 'PDF/A upload',
                                'DOI registration', 'Delivery diff',
                                'PDF/A diff','Publication online',
                                'Pub. online diff']) + '\n'

        for recid in papers:
            rec = get_record(recid)
            doi = get_doi(rec)
            first_del = None
            first_ab_del = None
            last_mod = None
            doi_reg = None
            pdfa_del = None
            first_del, first_ab_del, last_mod, doi_reg, pdfa_del, pub_date = get_delivery_data(recid, doi)

            record_compl = is_complete_record(recid)
            return_val += ';'.join(str(item) for item in [str(recid),
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
                                   is_compliant(recid, 'category').lstrip('<b>').rstrip('</b>'),
                                   str([rec_key for rec_key, rec_val in record_compl.iteritems() if not rec_val]).replace('\n',' ').replace(',',' '),
                                   str(first_del),
                                   str(first_ab_del),
                                   str(last_mod),
                                   str(pdfa_del),
                                   str(doi_reg),
                                   check_24h_delivery(first_del, doi_reg),
                                   check_24h_delivery(pdfa_del, doi_reg),
                                   str(pub_date),
                                   check_24h_delivery(first_del, pub_date),
                                   ])
            return_val += '\n'

    return return_val


def check_compliance_csv(req, collections='', from_date='', to_date='',
                         created_or_modified_date=''):
    req.content_type = 'text/csv; charset=utf-8'
    req.headers_out['content-disposition'] = ('attachment; '
                                              'filename=scoap3_compliance.csv')

    (pdfa_journals,
     no_pdfa_journals,
     no_xml_journals,
     from_date,
     to_date) = prepare_filter_variables(collections, from_date, to_date)

    tmp = (write_csv(req, JOURNALS_PDFA, pdfa_journals, from_date,
                     to_date, created_or_modified_date)
           + write_csv(req, JOURNALS_NO_PDFA, no_pdfa_journals, from_date,
                       to_date, created_or_modified_date)
           + write_csv(req, JOURNALS_NO_XML, no_xml_journals, from_date,
                       to_date, created_or_modified_date))

    print >> req, tmp
