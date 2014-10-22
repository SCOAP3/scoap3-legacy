from invenio.dbquery import run_sql
from invenio.bibtask import write_message

def prepare_package_table():
    return run_sql("""CREATE TABLE IF NOT EXISTS package (
        id mediumint NOT NULL AUTO_INCREMENT,
        name varchar(255) NOT NULL UNIQUE,
        delivery_date datetime NOT NULL,
        PRIMARY KEY doi(id),
        KEY (name)
    ) ENGINE=MyISAM;""")


def prepare_doi_package_table():
    return run_sql("""CREATE TABLE IF NOT EXISTS doi_package (
        package_id mediumint NOT NULL,
        doi varchar(255) NOT NULL,
        PRIMARY KEY doi_pacakge(package_id, doi),
        FOREIGN KEY (package_id)
            REFERENCES package(id)
            ON DELETE CASCADE,
        FOREIGN KEY (doi)
            REFERENCES doi(doi)
            ON DELETE CASCADE
    ) ENGINE=MyISAM;""")


def store_packages_deliveries(packages_deliveries):
    for p in packages_deliveries:
        name = p[0][:-1]
        date = p[1]
        if run_sql("SELECT name FROM package WHERE name=%s", (name, )):
            write_message("Package already exist: %s: %s" % ('Elsevier', name))
            continue
        else:
            write_message("New pacakge discovered for publisher %s: %s" % ('Elsevier', name))
            run_sql("INSERT INTO package(name, delivery_date) VALUES(%s, %s)", (name.strip(), date))


def store_doi_package_mappings(doi_package_name_mappings):
    for dp in doi_package_name_mappings:
        try:
            p_name, doi = dp
            p_id = run_sql("SELECT id FROM package WHERE name=%s", (p_name.strip(),))
            try:
                write_message("Adding doi to package: %d %s" % (p_id[0][0], doi))
                run_sql("INSERT INTO doi_package VALUES(%s, %s)", (p_id[0][0], doi))
            except Exception as e:
                write_message(e)
                write_message("This already exist: %d %s" % (p_id[0][0], doi))
        except Exception as e:
            write_message(e)


def run(package_obj, packages_deliveries, doi_package_name_mappings):
    package_obj.bibupload_it()

    prepare_package_table()
    prepare_doi_package_table()

    write_message(packages_deliveries)
    store_packages_deliveries(packages_deliveries)
    store_doi_package_mappings(doi_package_name_mapping)
    
