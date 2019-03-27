import unittest
from collections import Generator

from string_set import StringSet


class StringSetTest(unittest.TestCase):
    alphabet = ['a', 'b']
    avoid = ['aa', 'bb']
    ss = StringSet(alphabet, avoid)

    def test_is_generator(self):
        self.assertIsInstance(self.ss, Generator)

    def test_first_8_elements(self):
        actual_first_8_elmts = ['', 'a', 'b', 'ab', 'ba', 'aba', 'bab', 'abab']
        generator_first_8_elmts = [next(self.ss) for _ in range(8)]
        self.assertEqual(actual_first_8_elmts, generator_first_8_elmts)

    def test_next_string(self):
        self.assertEqual(self.ss.next_lexicographical_string(''), 'a')
        self.assertEqual(self.ss.next_lexicographical_string('a'), 'b')
        self.assertEqual(self.ss.next_lexicographical_string('b'), 'aa')

        self.assertEqual(self.ss.next_lexicographical_string('aa'), 'ab')
        self.assertEqual(self.ss.next_lexicographical_string('ab'), 'ba')
        self.assertEqual(self.ss.next_lexicographical_string('ba'), 'bb')

        self.assertEqual(self.ss.next_lexicographical_string('bb'), 'aaa')
        self.assertEqual(self.ss.next_lexicographical_string('aaa'), 'aab')

    def test_contains_string(self):
        self.assertFalse(self.ss.contains('aa'))
        self.assertFalse(self.ss.contains('bb'))
        self.assertFalse(self.ss.contains('abba'))
        self.assertFalse(self.ss.contains('bababaa'))

        self.assertTrue(self.ss.contains(''))
        self.assertTrue(self.ss.contains('a'))
        self.assertTrue(self.ss.contains('b'))
        self.assertTrue(self.ss.contains('ab'))
        self.assertTrue(self.ss.contains('bababa'))

    def test_equality(self):
        ss_eq = StringSet(self.alphabet, self.avoid)
        self.assertEqual(self.ss, ss_eq)

        reversed_alphabet = list(reversed(self.alphabet))
        ss_neq = StringSet(reversed_alphabet, self.avoid)
        self.assertNotEqual(self.ss, ss_neq)


if __name__ == '__main__':
    unittest.main()
