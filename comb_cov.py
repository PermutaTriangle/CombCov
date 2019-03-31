from exact_cover import exact_cover


class CombCov():

    def __init__(self, root_object, max_elmnt_size=9):
        self.root_object = root_object
        self.max_elmnt_size = max_elmnt_size
        self._enumerate_all_elmnts_up_to_max_size()
        self._create_binary_strings_from_rules()

        print("Trying to find a cover for '{}' up to size {} using {} self-generated rules.".format(self.root_object,
                                                                                                    self.max_elmnt_size,
                                                                                                    len(self.rules)))
        print("(Enumeration: {})".format(self.enumeration))
        self._find_cover()

        solutions = self.get_solutions()
        if solutions.__len__() > 0:
            print("SUCCESS! Found {} solution(s).".format(solutions.__len__()))
            for nr, solution in enumerate(solutions, start=1):
                print("Solution nr. {}:".format(nr))
                for rule in solution:
                    print(" - {}".format(rule))
        else:
            print("FAILURE. No solutions found.")

    def _enumerate_all_elmnts_up_to_max_size(self):
        elmnts = []
        self.enumeration = [None] * (self.max_elmnt_size + 1)
        for n in range(self.max_elmnt_size + 1):
            elmnts_of_length_n = self.root_object.of_length(n)
            self.enumeration[n] = len(elmnts_of_length_n)
            elmnts.extend(elmnts_of_length_n)

        self.elmnts_dict = {
            string: nr for nr, string in enumerate(elmnts, start=0)
        }

    def _create_binary_strings_from_rules(self):
        self.rules_dict = {}
        self.rules = self.root_object.rule_generator(max_string_length=self.max_elmnt_size)
        for rule in self.rules:
            binary_string = 0
            for elmnt in rule.get_elmnts():
                binary_string += 2 ** (self.elmnts_dict[elmnt])

            self.rules_dict[rule] = binary_string

    def _find_cover(self):
        self.solutions_indices = exact_cover(list(self.rules_dict.values()), len(self.elmnts_dict))

    def get_solutions_indices(self):
        return self.solutions_indices

    def get_solutions(self):
        solutions = []
        for solution_indices in self.get_solutions_indices():
            solution = [self.rules[binary_string] for binary_string in solution_indices]
            solutions.append(solution)

        return solutions
