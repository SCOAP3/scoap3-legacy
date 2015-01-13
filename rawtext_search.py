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

import re


class RawTextSearch:
    def __init__(self, searchstring, normal_search_delimiter="'",
                 regex_search_delimiter="/"):
        self.searchstring = searchstring

        self.normal_search_delimiter = normal_search_delimiter
        self.regex_search_delimiter = regex_search_delimiter

        self.operators = []
        self.operators.append((" ", "OR"))
        self.operators.append(("OR", "OR"))
        self.operators.append(("-", "NEG"))
        self.operators.append((self.normal_search_delimiter, "none"))
        self.operators.append((self.regex_search_delimiter, "none"))
        self.operators.append(("(", "LBR"))
        self.operators.append((")", "RBR"))

        self.rules = [
            ("NEGT", ("NEG", "ST")),
            ("ST", ("NEGT",), ("LBR", "OR", "RBR"), ("LBR", "ST", "RBR")),
            ("OR", ("ST", "OR", "ST"), ("OR", "OR", "ST"), ("ST", "OR", "OR"),
             ("OR", "OR", "OR"))
        ]

        self.pick_rules = {
            ("NEGT",): (0,),
            ("NEG", "ST"): (1,),
            ("LBR", "OR", "RBR"): (1,),
            ("LBR", "ST", "RBR"): (1,),
            ("ST", "OR", "ST"): (0, 2),
            ("OR", "OR", "ST"): (0, 2),
            ("ST", "OR", "OR"): (0, 2),
            ("OR", "OR", "OR"): (0, 2)
        }

        self.operator_actions = {
            "ST": self._st_action,
            "OR": self._or_action,
            "NEGT": self._neg_action
        }

        self.raw_splits = self._split()
        self.assigned_splits = self._assign_meanings(self.raw_splits)

        self.searchtree = self._build_search_tree(self.assigned_splits)

    def _st_action(self, results):
        return results[0]

    def _or_action(self, results):
        val = False
        for result in results:
            val = val or result
        return val

    def _neg_action(self, results):
        return not results[0]

    # SPLIT THE SEARCH INTO ATOMIC PARTS
    def _get_operator_length(self, operator, index):
        if operator[0] == self.normal_search_delimiter:
            next_pos = self.searchstring.find(self.normal_search_delimiter,
                                              index+1)
            return next_pos-index+len(operator[0])
        elif operator[0] == self.regex_search_delimiter:
            next_pos = self.searchstring.find(self.regex_search_delimiter,
                                              index+1)
            return next_pos-index+len(operator[0])
        else:
            return len(operator[0])

    def _operator_length(self, index):
        operator_length = 0
        for operator in self.operators:
            if operator[0] == self.searchstring[index:index+len(operator[0])]:
                return self._get_operator_length(operator, index)
        return operator_length

    def _split(self):
        splits = []

        i = 0
        while i < len(self.searchstring):
            operator_length = self._operator_length(i)
            if operator_length == 0:
                raise Exception(('Infinite loop while splitting the search '
                                 'string. Check your search_delimiters '
                                 'or the search string.'))
            splits.append(self.searchstring[i:i+operator_length])
            i += operator_length

        for i in range(len(splits)):
            if splits[i] == " ":
                splits[i] = "OR"

        return splits

    # ASSIGN MEANING TO THE ATOMIC PARTS
    def _assign_meanings(self, splits):
        new_splits = []
        for i in range(len(splits)):
            searchterm = True
            for operator in self.operators:
                if splits[i] == operator[0]:
                    searchterm = False
                    new_splits.append((operator[1], splits[i]))
            if searchterm:
                new_splits.append(("ST", splits[i]))
        return new_splits

    #BUILD THE SEARCH TREE
    def _fits_rule(self, subrule, index, new_splits):
        fits = True
        for i in range(len(subrule)):
            try:
                if subrule[i] != new_splits[index+i][0]:
                    fits = False
                    break
            except Exception:
                fits = False
                break
        return fits

    def _combine(self, rule, subrule, index, new_splits):
        tmp = new_splits
        new_tuple_list = [rule[0]]
        picks = self.pick_rules[subrule]
        for i in picks:
            new_tuple_list.append(new_splits[index+i])

        for i in range(len(subrule)):
            del(tmp[index])

        tmp.insert(index, tuple(new_tuple_list))

        return tmp

    def _build_search_tree(self, splits):
        new_splits = splits
        start_over = False
        while len(new_splits) != 1:
            start_over = False
            for rule in self.rules:
                for subrule in rule[1:]:
                    for i in range(len(new_splits)):
                        if self._fits_rule(subrule, i, new_splits):
                            new_splits = self._combine(rule,
                                                       subrule,
                                                       i,
                                                       new_splits)
                            start_over = True
                            break
                    if start_over:
                        break
                if start_over:
                    break
            if not start_over:
                raise Exception

        return new_splits[0]

    #PRINT TREE
    def _print_tree(self, new_split, indentation_level=0):
        indentation = ''
        for i in range(indentation_level):
            indentation += "\t"

        print indentation + new_split[0]
        for split in new_split[1:]:
            if isinstance(split, (list, tuple)):
                self._print_tree(split, indentation_level+1)
            else:
                print indentation + '\t' + split

    def print_tree(self, indentation_level=0):
        indentation = ''
        for i in range(indentation_level):
            indentation += "\t"

        print indentation + self.searchtree[0]
        for split in self.searchtree[1:]:
            if isinstance(split, (list, tuple)):
                self._print_tree(split, indentation_level+1)
            else:
                print indentation + '\t' + split

    #SEARCH STUFF
    def _is_regex(self, searchterm):
        if searchterm.startswith(self.regex_search_delimiter):
            return True
        return False

    def _get_active_operator(self, operator_string):
        return self.operator_actions[operator_string]

    def _clean_searchterm(self, searchterm):
        if searchterm.startswith(self.normal_search_delimiter):
            return searchterm.replace(self.normal_search_delimiter, '')
        if searchterm.startswith(self.regex_search_delimiter):
            return searchterm.replace(self.regex_search_delimiter, '')

        return searchterm

    def _perform_search(self, raw_text, searchterm):
        if not self._is_regex(searchterm):
            searchterm = self._clean_searchterm(searchterm)
            return searchterm in raw_text
        else:
            searchterm = self._clean_searchterm(searchterm)
            pattern = re.compile(searchterm, re.IGNORECASE)
            return pattern.search(raw_text) is not None

    def _search(self, raw_text, searchtree):
        active_operator = None
        results = []

        if isinstance(searchtree, (tuple)):
            active_operator = self._get_active_operator(searchtree[0])
            for sub_tree in searchtree[1:]:
                results.append(self._search(raw_text, sub_tree))
        else:
            return self._perform_search(raw_text, searchtree)

        return active_operator(results)

    def search(self, raw_text):
        active_operator = None
        results = []

        if isinstance(self.searchtree, (tuple)):
            active_operator = self._get_active_operator(self.searchtree[0])
            for sub_tree in self.searchtree[1:]:
                results.append(self._search(raw_text, sub_tree))
        else:
            return self._perform_search(raw_text, self.searchtree)

        return active_operator(results)
