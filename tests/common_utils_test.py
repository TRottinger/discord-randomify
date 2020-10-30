import unittest
from unittest import mock
from unittest import TestCase
from utils import common_utils


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, content):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content

        def json(self):
            return self.json_data

    if args[0] == 'https://www.mit.edu/~ecprice/wordlist.10000':
        return MockResponse({"key1": "value1"}, 200, "word".encode())
    elif args[0] == 'https://www.mit.edu/badworldlist':
        return MockResponse({"key1": "value1"}, 200, "".encode())
    return MockResponse(None, 404, "".encode())


class CommonUtilsTests(TestCase):
    @mock.patch('utils.common_utils.requests.get', side_effect=mocked_requests_get)
    def test_get_random_query(self, mock_get):
        rword = common_utils.get_random_query()
        self.assertIn(mock.call('https://www.mit.edu/~ecprice/wordlist.10000'), mock_get.call_args_list)
        self.assertEqual(rword, "word")

    @mock.patch('utils.common_utils.requests.get', side_effect=mocked_requests_get)
    def test_get_random_query_good_link(self, mock_get):
        rword = common_utils.get_random_query('https://www.mit.edu/~ecprice/wordlist.10000')
        self.assertIn(mock.call('https://www.mit.edu/~ecprice/wordlist.10000'), mock_get.call_args_list)
        self.assertEqual(rword, "word")

    @mock.patch('utils.common_utils.requests.get', side_effect=mocked_requests_get)
    def test_get_random_query_empty_return(self, mock_get):
        rword = common_utils.get_random_query('https://www.mit.edu/badworldlist')
        self.assertIn(mock.call('https://www.mit.edu/badworldlist'), mock_get.call_args_list)
        self.assertEqual(rword, "random")


if __name__ == '__main__':
    unittest.main()
