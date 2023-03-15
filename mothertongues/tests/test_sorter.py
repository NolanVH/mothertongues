from string import ascii_lowercase
from unittest import TestCase, main

from pandas import DataFrame

from mothertongues.processors.sorter import ArbSorter
from mothertongues.utils import add_sorting_form_to_df


class SorterTest(TestCase):
    def setUp(self):
        self.english_alphabet = list(ascii_lowercase)
        self.danish_alphabet = self.english_alphabet + ["æ", "ø", "å"]

    def list_to_sorting_form(self, lex_list, key="word"):
        """turn list of strings into list of dicts with sorting forms"""
        return [{key: v} for v in lex_list]

    def test_sort_ignorables(self):
        """Sort ignorable characters"""
        sorter = ArbSorter(self.danish_alphabet, ignorable=["ū"])
        lexicon = self.list_to_sorting_form(["råd", "ūįrød"])
        lexicon_sorted = [
            {"word": "råd", "sorting_form": [17, 28, 3]},
            {"word": "ūįrød", "sorting_form": [10000, 17, 27, 3]},
        ]
        self.assertEqual(sorter(lexicon, "word"), lexicon_sorted)
        self.assertEqual(sorter.values_as_word([10000, 17, 27, 3]), "įrød")

    def test_sort_oov_characters(self):
        """Sort oov characters at the end"""
        sorter = ArbSorter(self.danish_alphabet)
        lexicon = self.list_to_sorting_form(["råd", "ūįrød"])
        lexicon_sorted = [
            {"word": "råd", "sorting_form": [17, 28, 3]},
            {"word": "ūįrød", "sorting_form": [10000, 10001, 17, 27, 3]},
        ]
        self.assertEqual(sorter(lexicon, "word"), lexicon_sorted)
        self.assertEqual(sorter.values_as_word([10000, 10001, 17, 27, 3]), "ūįrød")

    def test_sort_unicode(self):
        """Sort non-ascii characters."""
        sorter = ArbSorter(self.danish_alphabet)
        lexicon = self.list_to_sorting_form(["æbleskiver", "hund", "råd", "rød"])
        lexicon_sorted = [
            {"word": "hund", "sorting_form": [7, 20, 13, 3]},
            {"word": "rød", "sorting_form": [17, 27, 3]},
            {"word": "råd", "sorting_form": [17, 28, 3]},
            {
                "word": "æbleskiver",
                "sorting_form": [26, 1, 11, 4, 18, 10, 8, 21, 4, 17],
            },
        ]
        self.assertEqual(sorter(lexicon, "word"), lexicon_sorted)

    def test_sort_unicode_df(self):
        """Sort non-ascii characters in DataFrame."""
        sorter = ArbSorter(self.danish_alphabet)
        lexicon = DataFrame(
            self.list_to_sorting_form(["æbleskiver", "hund", "råd", "rød"])
        )
        lexicon_sorted = DataFrame(
            [
                {
                    "word": "æbleskiver",
                    "sorting_form": [26, 1, 11, 4, 18, 10, 8, 21, 4, 17],
                },
                {"word": "hund", "sorting_form": [7, 20, 13, 3]},
                {"word": "råd", "sorting_form": [17, 28, 3]},
                {"word": "rød", "sorting_form": [17, 27, 3]},
            ]
        ).sort_values(by=["sorting_form"])["sorting_form"]
        self.assertTrue(
            lexicon_sorted.equals(
                add_sorting_form_to_df(lexicon, sorter, "word")["sorting_form"]
            )
        )

    def test_digraph_sorting(self):
        """Sort digraphs"""
        sorter = ArbSorter(["a", "b", "aa", "c"])
        lexicon = self.list_to_sorting_form(["aba", "aaba", "caba", "baca"])
        lexicon_sorted = [
            {"word": "aba", "sorting_form": [0, 1, 0]},
            {"word": "baca", "sorting_form": [1, 0, 3, 0]},
            {"word": "aaba", "sorting_form": [2, 1, 0]},
            {"word": "caba", "sorting_form": [3, 0, 1, 0]},
        ]
        self.assertEqual(lexicon_sorted, sorter(lexicon, "word"))


if __name__ == "__main__":
    main()
