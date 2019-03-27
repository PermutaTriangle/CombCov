from collections import Generator


class StringSet(Generator):
    """The set of strings over alphabet ∑ avoiding a set of strings A."""

    def __init__(self, alphabet=['a', 'b'], avoid=[]):
        self.alphabet = alphabet
        self.avoid = avoid

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

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, StringSet):
            return (self.alphabet == other.alphabet and self.avoid == other.avoid)
        return False
