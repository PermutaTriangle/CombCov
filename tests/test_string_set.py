import unittest
from collections import Generator

from string_set import Rule, StringSet


class StringSetTest(unittest.TestCase):
    alphabet = ['a', 'b']
    avoid = ['aa', 'bb']
    avoid_subset = ['bb']

    def test_is_generator(self):
        string_set = StringSet(self.alphabet, self.avoid)
        self.assertIsInstance(string_set, Generator)

    def test_first_8_elements(self):
        string_set = StringSet(self.alphabet, self.avoid)
        actual_first_8_elmts = ['', 'a', 'b', 'ab', 'ba', 'aba', 'bab', 'abab']
        generator_first_8_elmts = [next(string_set) for _ in range(8)]
        self.assertListEqual(actual_first_8_elmts, generator_first_8_elmts)

    def test_next_string(self):
        string_set = StringSet(self.alphabet, self.avoid)

        self.assertEqual(string_set.next_lexicographical_string(''), 'a')
        self.assertEqual(string_set.next_lexicographical_string('a'), 'b')
        self.assertEqual(string_set.next_lexicographical_string('b'), 'aa')

        self.assertEqual(string_set.next_lexicographical_string('aa'), 'ab')
        self.assertEqual(string_set.next_lexicographical_string('ab'), 'ba')
        self.assertEqual(string_set.next_lexicographical_string('ba'), 'bb')

        self.assertEqual(string_set.next_lexicographical_string('bb'), 'aaa')
        self.assertEqual(string_set.next_lexicographical_string('aaa'), 'aab')

    def test_contains_string(self):
        string_set = StringSet(self.alphabet, self.avoid)

        self.assertFalse(string_set.contains('aa'))
        self.assertFalse(string_set.contains('bb'))
        self.assertFalse(string_set.contains('abba'))
        self.assertFalse(string_set.contains('bababaa'))

        self.assertTrue(string_set.contains(''))
        self.assertTrue(string_set.contains('a'))
        self.assertTrue(string_set.contains('b'))
        self.assertTrue(string_set.contains('ab'))
        self.assertTrue(string_set.contains('bababa'))

    def test_sunny_strings_of_length(self):
        string_set = StringSet(self.alphabet, self.avoid)
        length_five_strings = string_set.of_length(5)
        actual_valid_strings = ['ababa', 'babab']
        self.assertListEqual(length_five_strings, actual_valid_strings)

    def test_rainy_strings_of_length(self):
        string_set = StringSet(self.alphabet, self.avoid)
        length_zero_strings = string_set.of_length(0)
        self.assertListEqual(length_zero_strings, [''])

        negative_length_strings = string_set.of_length(-1)
        self.assertListEqual(negative_length_strings, [])

    def test_all_substrings_of_string(self):
        string = 'aba'
        substrings = StringSet._get_all_substrings_of(string)
        expected_substrings = ['a', 'ab', 'aba', 'b', 'ba']
        self.assertEqual(expected_substrings, substrings)

    def test_avoiding_subsets(self):
        string_set = StringSet(self.alphabet, self.avoid)
        expected_subsets = {frozenset({"aa", "bb"}), frozenset({"aa", "b"}), frozenset({"a", "bb"}),
                            frozenset({'a', 'b'})}
        subsets = string_set.get_all_avoiding_subsets()
        self.assertEqual(expected_subsets, subsets)

    def test_rule_creation(self):
        string_set = StringSet(self.alphabet, self.avoid)

        prefix = "ab"
        max_string_length = 4
        avoiding_subset = ['bb']
        sub_string_set = StringSet(self.alphabet, avoiding_subset)

        rule = Rule(prefix, sub_string_set, max_string_length)
        self.assertGreaterEqual(max_string_length, max(len(elmnt) for elmnt in rule.get_elmnts()))

        expected_rule = frozenset(['ab', 'aba', 'abb', 'abaa', 'abab', 'abba'])
        self.assertEqual(rule.get_elmnts(), expected_rule)
        self.assertFalse(string_set.accept_rule(rule))

    def test_rule_generation(self):
        string_set = StringSet(self.alphabet, self.avoid)
        rules = string_set.rule_generator(prefix_size=3, max_string_length=9)

        self.assertNotIn(None, rules)
        self.assertTrue(all(string_set.accept_rule(rule) for rule in rules))

    def test_equality(self):
        string_set = StringSet(self.alphabet, self.avoid)
        string_set_eq = StringSet(self.alphabet, self.avoid)
        self.assertEqual(string_set, string_set_eq)

    def test_equality_reversed_alphabet(self):
        string_set = StringSet(self.alphabet, self.avoid)
        string_set_rev = StringSet(list(reversed(self.alphabet)), self.avoid)
        self.assertNotEqual(string_set, string_set_rev)

    def test_equality_reversed_avoidance(self):
        string_set = StringSet(self.alphabet, self.avoid)
        string_set_rev = StringSet(self.alphabet, list(reversed(self.avoid)))
        self.assertEqual(string_set, string_set_rev)

    def test_equality_nonsense(self):
        string_set = StringSet(self.alphabet, self.avoid)
        self.assertNotEqual(string_set, "nonsense")
        self.assertNotEqual(string_set, None)


if __name__ == '__main__':
    unittest.main()
