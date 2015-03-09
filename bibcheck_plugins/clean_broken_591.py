# -*- coding: utf-8 -*-
#
# This file is part of SCOAP3.
# Copyright (C) 2015 CERN.

# SCOAP3 is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.

# SCOAP3 is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SCOAP3; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.


def check_records(records):
    for rec in records:
        indexes_to_delete = []
        if '591' in rec:
            for i, field in enumerate(rec['591']):
                if not field[0]:
                    indexes_to_delete.append(i)
            if indexes_to_delete:
                for index in reversed(sorted(indexes_to_delete)):
                    del rec['591'][index]
                rec.set_amended("%s empty '591' fields removed." % (len(indexes_to_delete)))
