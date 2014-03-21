import re

class RawTextSearch:
    def __init__(self, searchstring):
        self.searchstring = searchstring

        self.operators = []
        self.operators.append((" ", "OR"))
        self.operators.append(("OR", "OR"))
        self.operators.append(("-", "NEG"))
        self.operators.append(('\'', "none"))
        self.operators.append(('/', "none"))
        self.operators.append(("(", "LBR"))
        self.operators.append((")", "RBR"))

        self.rules = [
            ("NEGT", ("NEG", "ST")),
            ("ST", ("NEGT",), ("LBR", "OR", "RBR"), ("LBR", "ST", "RBR")),
            ("OR", ("ST", "OR", "ST"), ("OR", "OR", "ST"), ("ST", "OR", "OR"), ("OR", "OR", "OR"))
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
            "ST": self.__st_action,
            "OR": self.__or_action,
            "NEGT": self.__neg_action
        }

        self.raw_splits = self.__split()
        self.assigned_splits = self.__assign_meanings(self.raw_splits)

        self.searchtree = self.__build_search_tree(self.assigned_splits)

    def __st_action(self, results):
        return results[0]

    def __or_action(self, results):
        val = False
        for result in results:
            val = val or result
        return val

    def __neg_action(self, results):
        return not results[0]

    # SPLIT THE SEARCH INTO ATOMIC PARTS
    def __is_operator(self, index):
        operator_length = 0
        for operator in self.operators:
            if operator[0] == self.searchstring[index:index+len(operator[0])]:
                if operator[0] == '\'':
                    next_position = self.searchstring.find('\'', index+1)
                    return next_position-index+1
                elif operator[0] == '/':
                    next_position = self.searchstring.find('/', index+1)
                    return next_position-index+1
                else:
                    return len(operator[0])
        return operator_length

    def __is_searchterm(self, index):
        substring = self.searchstring[index:]
        for i in range(len(substring)):
            char = substring[i]
            if is_operator(i, substring):
                return i
        return len(substring)

    def __split(self):
        splits = []

        i = 0
        while i < len(self.searchstring):
            char = self.searchstring[i]
            operator_length = self.__is_operator(i)
            if operator_length > 0:
                splits.append(self.searchstring[i:i+operator_length])
                i += operator_length
            else:
                searchterm_length = self.__is_searchterm(i, searchstring)
                splits.append(self.searchstring[i:i+searchterm_length])
                i += searchterm_length

        for i in range(len(splits)):
            if splits[i] == " ":
                splits[i] = "OR"

        return splits

    # ASSIGN MEANING TO THE ATOMIC PARTS
    def __assign_meanings(self, splits):
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
    def __fits_rule(self, subrule, index, new_splits):
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

    def __combine(self, rule, subrule, index, new_splits):
        tmp = new_splits
        new_tuple_list = [rule[0]]
        picks = self.pick_rules[subrule]
        for i in picks:
            new_tuple_list.append(new_splits[index+i])

        for i in range(len(subrule)):
            del(tmp[index])

        tmp.insert(index, tuple(new_tuple_list))

        return tmp

    def __build_search_tree(self, splits):
        new_splits = splits
        start_over = False
        while len(new_splits) != 1:
            start_over = False
            for rule in self.rules:
                for subrule in rule[1:]:
                    for i in range(len(new_splits)):
                        if self.__fits_rule(subrule, i, new_splits):
                            new_splits = self.__combine(rule,
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
    def __print_tree(self, new_split, indentation_level=0):
        indentation = ''
        for i in range(indentation_level):
            indentation += "\t"

        print indentation + new_split[0]
        for split in new_split[1:]:
            if isinstance(split, (list, tuple)):
                self.__print_tree(split, indentation_level+1)
            else:
                print indentation + '\t' + split

    def print_tree(self, indentation_level=0):
        indentation = ''
        for i in range(indentation_level):
            indentation += "\t"

        print indentation + self.searchtree[0]
        for split in self.searchtree[1:]:
            if isinstance(split, (list, tuple)):
                self.__print_tree(split, indentation_level+1)
            else:
                print indentation + '\t' + split

    #SEARCH STUFF
    def __is_regex(self, searchterm):
        if searchterm[0] == '/':
            return True
        return False

    def __get_active_operator(self, operator_string):
        return self.operator_actions[operator_string]

    def __clean_searchterm(self, searchterm):
        if searchterm[0] == "'" or searchterm[0] == "/":
            return searchterm[1:len(searchterm)-1]
        return searchterm

    def __perform_search(self, raw_text, searchterm):
        if not self.__is_regex(searchterm):
            searchterm = self.__clean_searchterm(searchterm)
            return searchterm in raw_text
        else:
            searchterm = self.__clean_searchterm(searchterm)
            pattern = re.compile(searchterm, re.IGNORECASE)
            return pattern.search(raw_text) is not None

    def __search(self, raw_text, searchtree):
        active_operator = None
        results = []

        if isinstance(searchtree, (tuple)):
            active_operator = self.__get_active_operator(searchtree[0])
            for sub_tree in searchtree[1:]:
                results.append(self.__search(raw_text, sub_tree))
        else:
            return self.__perform_search(raw_text, searchtree)

        return active_operator(results)

    def search(self, raw_text):
        active_operator = None
        results = []

        if isinstance(self.searchtree, (tuple)):
            active_operator = self.__get_active_operator(self.searchtree[0])
            for sub_tree in self.searchtree[1:]:
                results.append(self.__search(raw_text, sub_tree))
        else:
            return perform_search(raw_text, self.searchtree)

        return active_operator(results)


if __name__ == '__main__':
    print 'Running some tests...'
    # searchstring1 = "-'CC-BY' -'CC BY' -'Creative Commons Attribution'"
    searchstring1 = "-('CC-BY' 'CC BY' 'Creative Commons Attribution')"
    searchstring2 = "-'funded by SCOAP'"
    searchstring3 = "-(/(c|\(c\)) the author/ 'copyright cern')"
    searchstring4 = "/(copyright|c)[^.]*(IOP|Institute of Physics)/"

    search1 = RawTextSearch(searchstring1)
    search2 = RawTextSearch(searchstring2)
    search3 = RawTextSearch(searchstring3)
    search4 = RawTextSearch(searchstring4)

    search1.print_tree()
    search2.print_tree()
    search3.print_tree()
    search4.print_tree()

    raw_text1 = '''
       CC BY Banana
       Open Access, c The Authors, (c) The Authors.
       Article funded by SCOAP3.
       c . Institute of Physics.
       '''

    raw_text2 = '''
        Open Access
        Article by SCOAP3.
        c blah blah Institute of Physics.
    '''

    print "For the following text everything should be false"
    print raw_text1
    print search1.search(raw_text1)
    print search2.search(raw_text1)
    print search3.search(raw_text1)
    print search4.search(raw_text1)

    print "For the following text everything should be false"
    print raw_text2
    print search1.search(raw_text2)
    print search2.search(raw_text2)
    print search3.search(raw_text2)
    print search4.search(raw_text2)
