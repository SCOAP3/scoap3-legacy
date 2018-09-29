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

#!/usr/bin/env python
from cgi import escape
from bs4 import BeautifulSoup
from urllib import urlopen

## DOIs da includere in first articles.

URL = "http://link.springer.com/journal/10052/74/1/page/1"

soup = BeautifulSoup(urlopen(URL).read())
articles = soup.findAll('h3', {'class': 'title'})
print "<p><ul>"
for article in articles:
    article = article.find('a')
    href = article.get('href')
    doi = href.replace("/article/", "").encode('utf8')
    title = article.getText(' ', True).strip().encode('utf8')
    print '<li><a href="https://doi.org/%s" target="_blank">%s</a>: %s</li>' % (escape(doi, True), escape(doi), title)
print "</ul></p>"
