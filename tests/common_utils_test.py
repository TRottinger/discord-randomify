import unittest
from unittest import mock
from unittest import TestCase
from utils import common_utils


# This method will be used by the mock to replace requests.get
def mocked_setup_words(url=None):
    return ['word'.encode()]


def mocked_setup_words_empty(url=None):
    return []


class CommonUtilsTests(TestCase):
    @mock.patch('utils.common_utils.setup_words', side_effect=mocked_setup_words)
    def test_get_random_query(self, mock_get):
        test_random_query = common_utils.RandomQuery()
        rword = test_random_query.get_random_query()
        self.assertEqual(rword, "word")

    @mock.patch('utils.common_utils.setup_words', side_effect=mocked_setup_words)
    def test_get_random_query_strict(self, mock_get):
        test_random_query = common_utils.RandomQuery()
        rword = test_random_query.get_random_query_strict()
        self.assertEqual(rword, "word")

    @mock.patch('utils.common_utils.setup_words', side_effect=mocked_setup_words)
    def test_get_random_first_name(self, mock_get):
        test_random_query = common_utils.RandomQuery()
        rname = test_random_query.get_random_first_name()
        self.assertEqual(rname, "word")

    @mock.patch('utils.common_utils.setup_words', side_effect=mocked_setup_words_empty)
    def test_get_random_query_empty(self, mock_get):
        test_random_query = common_utils.RandomQuery()
        rword = test_random_query.get_random_query()
        self.assertEqual(rword, "random")

    @mock.patch('utils.common_utils.setup_words', side_effect=mocked_setup_words_empty)
    def test_get_random_query_strict_empty(self, mock_get):
        test_random_query = common_utils.RandomQuery()
        rword = test_random_query.get_random_query_strict()
        self.assertEqual(rword, "random")

    @mock.patch('utils.common_utils.setup_words', side_effect=mocked_setup_words_empty)
    def test_get_random_first_name_empty(self, mock_get):
        test_random_query = common_utils.RandomQuery()
        rname = test_random_query.get_random_first_name()
        self.assertEqual(rname, "Tim")


if __name__ == '__main__':
    unittest.main()
