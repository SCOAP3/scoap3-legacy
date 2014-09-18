from invenio.search_engine import get_collection_reclist
from invenio.utils import flatten_list

journals = ['Acta',
            'Advances in High Energy Physics',
            'Chinese Physics C',
            'Journal of Cosmology and Astroparticle Physics',
            'New Journal of Physics']

rec_ids = map(str, flatten_list(map(get_collection_reclist, journals)))


def has_field(field, subfield):
    for x in field:
        if x[0] == subfield:
            return True
    return False


def check_records(records, empty=False):
    fields = ['100', '700']

    for record in records:
        if record.record_id in rec_ids:
            for field in fields:
                if field in record:
                    for i, x in enumerate(record[field]):
                        data = x[0]
                        if has_field(data, 'v'):
                            continue
                        for new_field in filter(lambda x: x[0] == 'u', data):
                            record.add_subfield((field + '__v', i, 0),
                                                'v', new_field[1])
                            data.remove(new_field)
