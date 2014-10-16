import re

from xml.dom.minidom import parse

from harvestingkit.minidom_utils import xml_to_text
from invenio.utils import get_doc_ids, get_filenames_from_directory


def get_latest_file(path):
    files = get_filenames_from_directory(path, 'xml')
    return sorted(files, key=lambda x: int(x.split(';')[1]))[-1]


def has_field(field, subfield):
    field = field[0]
    for x in field:
        if x[0] == subfield:
            return True
    return False


def _get_index(author, key):
    author = author[0]
    for i, (_key, _) in enumerate(author):
        if key == _key:
            return i


def _get_orcids(xml_doc):
    result = []

    xml_authors = xml_doc.getElementsByTagName("ce:author")
    for xml_author in xml_authors:
        try:
            orcid = xml_author.getAttribute('orcid')
            if orcid:
                result.append('ORCID:{0}'.format(orcid))
            else:
                result.append('')
        except IndexError:
            result.append('')

        return result

    xml_authors = xml_doc.getElementsByTagName("contrib")
    for xml_author in xml_authors:
        try:
            contrib_id = xml_author.getElementsByTagName('contrib-id')[0]
            if contrib_id.getAttribute('contrib-id-type') == 'orcid':
                orcid_raw = xml_to_text(contrib_id)
                pattern = '\d\d\d\d-\d\d\d\d-\d\d\d\d-\d\d\d[\d|X]'
                result.append(re.search(pattern, orcid_raw).group())
        except (IndexError, AttributeError):
            result.append('')

    return result


def _add_orcid(record, author, field, i, orcid):
    if orcid:
        orcid = 'ORCID:{0}'.format(orcid)
        if has_field(author, 'j'):
            j = _get_index(author, 'j')
            record.amend_field((field+'__j', i, j), orcid)
        else:
            record.add_subfield((field+'__j', i, 0), 'j', orcid)


def check_records(records, empty=False):
    filepath = "/opt/invenio/var/data/files/g0/"

    for record in records:
        doc_ids = get_doc_ids(int(record.record_id))
        for doc_id in doc_ids:
            try:
                latest_file = get_latest_file(filepath + str(doc_id) + '/')
                xml = parse(latest_file)
            except:
                # DEEPLY sorry for the next line...
                continue

            orcids = _get_orcids(xml)

            try:
                for i, (orcid, author) in enumerate(zip(orcids[:1],
                                                        record['100'])):
                    _add_orcid(record, author, '100', i, orcid)
            except KeyError:
                pass

            try:
                for i, (orcid, author) in enumerate(zip(orcids[1:],
                                                        record['700'])):
                    _add_orcid(record, author, '700', i, orcid)
            except KeyError:
                pass

