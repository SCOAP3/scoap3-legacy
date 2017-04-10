from invenio.bibtask import task_update_progress, write_message
from invenio.dbquery import run_sql
from urllib import urlencode
from urllib2 import urlopen
from invenio.search_engine import perform_request_search, get_record
import json
import time
from invenio.bibrecord import record_get_field_value

CFG_RECORDS_PER_REQUEST = 10


def prepare_citation_table():
    run_sql("""CREATE TABLE IF NOT EXISTS citation (
        recid varchar(255) NOT NULL,
        citation_count int,
        PRIMARY KEY citation(recid),
        KEY (citation_count)
    ) ENGINE=MyISAM;""")

def bst_get_citations_count(reset=0):
    prepare_citation_table()
    recids = perform_request_search()
    for i, recid in enumerate(recids):
        doi = record_get_field_value(get_record(recid),'024','7','%','a')
        task_update_progress("Updating: {0}%".format(i*100/len(recids)))
        write_message("Getting record info for {0} with DOI:{1}".format(recid, doi))
        try:
            time.sleep(2)
            response = urlopen("http://inspirehep.net/search?ln=en&{0}&of=recjson&action_search=Search&sf=earliestdate&so=d".format(urlencode({'p':'0247_a:'+doi})))
            record_info = json.loads(response.read())
            citation_count = record_info[0]['number_of_citations']
            write_message(citation_count)
            if run_sql("SELECT citation_count FROM citation WHERE recid={0}".format(recid)):
                run_sql("UPDATE citation SET citation_count={0} WHERE recid={1}".format(citation_count, recid))
            else:
                write_message("Adding new citation count.")
                run_sql("INSERT INTO citation(recid, citation_count) VALUES({0}, {1})".format(recid, citation_count))
        except Exception as e:
            write_message(e)
