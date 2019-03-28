from collections import Generator


class StringSet(Generator):
    """The set of strings over alphabet ∑ avoiding a set of strings A."""

    def __init__(self, alphabet=['a', 'b'], avoid=set()):
        self.alphabet = alphabet
        self.avoid = frozenset(avoid)

        # Relating to the generator function
        self._nr = 0
        self._last_string = None

    def __str__(self):
        return "Av({}) over ∑={{{}}}".format(",".join(self.avoid), ",".join(self.alphabet))

    def next_lexicographical_string(self, from_string):
        if from_string is None:
            return ""

        else:
            str = list(from_string)

            # Increasing last character by one wand carry over if needed
            for i in range(len(str)):
                pos = -(i + 1)
                char = str[pos]
                index = self.alphabet.index(char)
                next_index = index + 1
                if next_index == len(self.alphabet):
                    str[pos] = self.alphabet[0]
                    # ...and carry one over
                else:
                    str[pos] = self.alphabet[next_index]
                    return "".join(str)

            # If we get this far we need to increase the length of the string
            return self.alphabet[0] + "".join(str)

    def contains(self, str):
        return all(av not in str for av in self.avoid)

    def send(self, ignored_arg):
        while True:
            next_string = self.next_lexicographical_string(self._last_string)
            self._last_string = next_string
            if self.contains(next_string):
                # Relies on this being an infinite set
                self._nr += 1
                return next_string

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def of_length(self, n=0):
        strings_of_length = []
        string_to_consider = self.alphabet[0] * n

        while len(string_to_consider) == n:
            if self.contains(string_to_consider):
                strings_of_length.append(string_to_consider)
            string_to_consider = self.next_lexicographical_string(string_to_consider)

        return strings_of_length

    @staticmethod
    def _get_all_substrings_of(s):
        return sorted(list(set(s[i:j + 1] for i in range(len(s)) for j in range(i, len(s)))))

    # TODO: This is an approximation, need to make it correct before running more complex examples
    def get_all_avoiding_subsets(self):
        avoiding_substrings = set()
        for string in self.avoid:
            subset_of_avoid = set(self.avoid.copy())
            subset_of_avoid.remove(string)
            for substring in self._get_all_substrings_of(string):
                subset_of_avoid_with_substring = subset_of_avoid.copy()
                subset_of_avoid_with_substring.add(substring)
                if subset_of_avoid_with_substring not in avoiding_substrings:
                    avoiding_substrings.add(frozenset(subset_of_avoid_with_substring))

        return avoiding_substrings

    def create_rule(self, prefix, string_set, max_string_length):
        rule = []
        for n in range(max_string_length - len(prefix) + 1):
            for elmnt in string_set.of_length(n):
                string = prefix + elmnt
                if string_set.contains(string):
                    rule.append(string)

        return rule

    def accept_rule(self, rule):
        return all(self.contains(string) for string in rule)

    def rule_generator(self, prefix_size=3, max_string_length=9):
        prefixes = []
        for n in range(prefix_size):
            prefixes += self.of_length(n + 1)

        rules = []
        for prefix in prefixes:
            for avoiding_subset in self.get_all_avoiding_subsets():
                sub_string_set = StringSet(self.alphabet, avoiding_subset)
                rule = self.create_rule(prefix, sub_string_set, max_string_length)
                rules.append(rule if self.accept_rule(rule) else None)

        return rules

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, StringSet):
            return (self.alphabet == other.alphabet and self.avoid == other.avoid)
        return False
