PREFIX = `python -c "from invenio.config import CFG_PREFIX; print CFG_PREFIX"`
LIBDIR = $(PREFIX)/lib
ETCDIR = $(PREFIX)/etc
WWWDIR = $(PREFIX)/var/www
APACHE = `python -c "from invenio.bibtask import guess_apache_process_user; print guess_apache_process_user()"`
#APACHE = www-data
#APACHE = wojciech
INSTALL = install -g $(APACHE)

scoap3tests = scoap3_unit_tests.py
templates = websearch_templates_scoap3.py webstyle_templates_scoap3.py webinterface_layout.py
utils = rawtext_search.py utils.py
bibtasklets = bst_doi_timestamp.py bst_fix_ffts.py
bibcheck_rules = rules.cfg
bibcheck_plugins = crossref_timestamp.py iop_issn.py iop_arxive_fix.py arxiv_prefix.py chk_add_publisher.py chk_fix_cc_by.py chk_add_inspireid.py compliance_check.py chk_fix_latex.py chk_find_erratum.py check_nations.py
bibexport_config = sitemap.cfg
bibformat_elements = bfe_publi_info.py
bibformat_templates = Default_HTML_actions.bft Default_HTML_detailed.bft Default_HTML_brief.bft
www_scripts = nations.py ffts_for_inspire.py compliance.py tools.py

elsevier_data_files = $(PREFIX)/var/data/scoap3/elsevier
elsevier_ready_packages = $(PREFIX)/var/data/scoap3/elsevier/ready_pkgs
elsevier_tar_files = $(PREFIX)/var/data/scoap3/elsevier/tar_files
springer_data_files = $(PREFIX)/var/data/scoap3/springer
springer_tar_files = $(PREFIX)/var/data/scoap3/springer/tar_files
springer_epjc_files = $(PREFIX)/var/data/scoap3/springer/tar_files/EPJC
springer_jhep_files = $(PREFIX)/var/data/scoap3/springer/tar_files/JHEP
oxford_data_files = $(PREFIX)/var/data/scoap3/oxford
oxford_tar_files = $(PREFIX)/var/data/scoap3/oxford/tar_files
oxford_unpacked_files = $(PREFIX)/var/data/scoap3/oxford/unpacked_files


install:
	$(INSTALL) -t $(LIBDIR)/python/invenio $(scoap3tests)
	$(INSTALL) -t $(LIBDIR)/python/invenio $(templates)
	$(INSTALL) -t $(LIBDIR)/python/invenio $(utils)
	$(INSTALL) -t $(ETCDIR)/bibcheck $(bibcheck_rules)
	$(INSTALL) -t $(LIBDIR)/python/invenio/bibcheck_plugins $(bibcheck_plugins)
	$(INSTALL) -t $(LIBDIR)/python/invenio/bibsched_tasklets $(bibtasklets)
	$(INSTALL) -t $(ETCDIR)/bibformat/format_templates $(bibformat_templates)
	$(INSTALL) -t $(LIBDIR)/python/invenio/bibformat_elements $(bibformat_elements)
	$(INSTALL) -t $(ETCDIR)/bibexport $(bibexport_config)

	$(INSTALL) -t $(WWWDIR) robots.txt
	$(INSTALL) -t $(WWWDIR) $(www_scripts)
	$(INSTALL) -t $(WWWDIR)/img scoap3_logo.png favicon.ico invenio_scoap3.css
	$(INSTALL) -d $(elsevier_data_files)
	$(INSTALL) -d $(elsevier_ready_packages)
	$(INSTALL) -d $(elsevier_tar_files)
	$(INSTALL) -d $(springer_data_files)
	$(INSTALL) -d $(springer_tar_files)
	$(INSTALL) -d $(springer_epjc_files)
	$(INSTALL) -d $(springer_jhep_files)
	$(INSTALL) -d $(oxford_data_files)
	$(INSTALL) -d $(oxford_tar_files)
	$(INSTALL) -d $(oxford_unpacked_files)

install-conf:
	$(INSTALL) -t $(ETCDIR) invenio-local.conf
