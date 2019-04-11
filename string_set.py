import itertools
from collections import Generator


class Rule:
    def __init__(self, prefix, string_set, max_string_length):
        self.prefix = prefix
        self.string_set = string_set
        self.max_string_length = max_string_length

        self.strings = []
        for n in range(max_string_length - len(prefix) + 1):
            for elmnt in string_set.of_length(n):
                self.strings.append(prefix + elmnt)

    def get_elmnts(self):
        return frozenset(self.strings)

    def __str__(self):
        return "'{}'*{}".format(self.prefix, self.string_set)


class StringSet(Generator):
    """The set of strings over alphabet ∑ avoiding a set of strings A."""

    def __init__(self, alphabet=list(), avoid=frozenset()):
        self.alphabet = list(alphabet)
        self.avoid = frozenset(avoid)
        if self.avoid is not frozenset():
            self.max_prefix_size = max(len(av) for av in self.avoid)
        else:
            self.max_prefix_size = 0

        # Relating to the generator function
        self._nr = 0
        self._last_string = None

    def __str__(self):
        return "Av({}) over ∑={{{}}}".format(",".join(self.avoid), ",".join(self.alphabet))

    def next_lexicographical_string(self, from_string):
        if from_string is None:
            return ""

        else:
            string = list(from_string)

            # Increasing last character by one and carry over if needed
            for i in range(len(string)):
                pos = -(i + 1)
                char = string[pos]
                index = self.alphabet.index(char)
                next_index = index + 1
                if next_index == len(self.alphabet):
                    string[pos] = self.alphabet[0]
                    # ...and carry one over
                else:
                    string[pos] = self.alphabet[next_index]
                    return "".join(string)

            # If we get this far we need to increase the length of the string
            return self.alphabet[0] + "".join(string)

    def contains(self, string):
        return all(av not in string for av in self.avoid)

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
        # list of set because we don't want duplicates
        return sorted(list(set(s[i:j + 1] for i in range(len(s)) for j in range(i, len(s)))))

    def get_all_avoiding_subsets(self):
        avoiding_substrings = [self._get_all_substrings_of(avoid) for avoid in self.avoid]
        return {frozenset(product) for product in itertools.product(*avoiding_substrings)}

    def accept_rule(self, rule):
        return rule.get_elmnts() is not frozenset() and all(self.contains(string) for string in rule.get_elmnts())

    def rule_generator(self, max_string_length=0):
        rules = []
        prefixes = []
        for n in range(self.max_prefix_size):
            prefixes.extend(self.of_length(n + 1))

        # Singleton rules, on the form prefix + empty StringSet
        for prefix in [''] + prefixes:
            empty_string_set = StringSet(alphabet=self.alphabet, avoid=frozenset(self.alphabet))
            rule = Rule(prefix=prefix, string_set=empty_string_set, max_string_length=len(prefix))
            if self.accept_rule(rule):
                rules.append(rule)

        # Regular rules of the from prefix + non-empty StringSet
        for prefix in prefixes:
            for avoiding_subset in self.get_all_avoiding_subsets():
                substring_set = StringSet(self.alphabet, avoiding_subset)
                rule = Rule(prefix, substring_set, max_string_length)
                if self.accept_rule(rule):
                    rules.append(rule)

        return rules

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, StringSet):
            return (self.alphabet == other.alphabet and self.avoid == other.avoid)
        return False
