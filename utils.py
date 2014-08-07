from os import listdir
from os.path import (isfile, join)
from collections import Iterable


from invenio.search_engine import get_record
from invenio.bibdocfile import BibRecDocs


#SCOAP3 related
def get_doi(recid):
    return sorted(get_record(recid)['024'][0][0],
                  key=lambda x: 1 if x[0] == 'a' else 2)[0][1]


def get_doc_ids(recid):
    return [bibdoc.get_id() for bibdoc in BibRecDocs(recid).list_bibdocs()]


def get_arxiv(recid):
    return sorted(get_record(recid)['037'][0][0],
                  key=lambda x: 1 if x[0] == 'a' else 2)[0][1]


def get_publisher(recid):
    return sorted(get_record(recid)['773'][0][0],
                  key=lambda x: 1 if x[0] == 'a' else 2)[0][1]


def get_latest_pdf(bibrec_latest_files):
    for file in bibrec_latest_files:
        if file.format == '.pdf' or file.format == '.pdf;pdfa':
            return file
    return None


def get_rawtext_from_record_id(record_id):
    bibrec = BibRecDocs(record_id)
    bibdoc = get_latest_pdf(bibrec.list_latest_files())
    try:
        rawtext = bibdoc.bibdoc.get_text()
    except:
        return ''

    return rawtext


def amend_fields(record, field, changes_dict, comment=''):
    """record : AmendableRecord"""
    for position, value in record.iterfield(field):
        key = value[:value.find(':')]
        if key in changes_dict:
            record.amend_field(position,
                               '%s:%d' % (key, changes_dict[key]),
                               comment)


def add_fields(record, field, subfield, value_dict):
    """record : AmendableRecord"""
    for key, value in value_dict.iteritems():
        record.add_field(field,
                         value="",
                         subfields=[(subfield, '%s:%d' % (key, value))])


#GENERAL
def get_filenames_from_directory(dirname, _filter=''):
    return [join(dirname, f) for f in listdir(dirname)
            if isfile(join(dirname, f)) and _filter in f]


def flatten_list(l):
    tmp = []
    if isinstance(l, Iterable) and not isinstance(l, basestring):
        for sl in l:
            tmp.extend(flatten_list(sl))
    else:
        return [l]

    return tmp


def build_path(file_path):
    pass


def split_path(file_path):
    pass
