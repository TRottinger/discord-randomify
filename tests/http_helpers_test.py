import unittest
from unittest import TestCase, mock
from utils import http_helpers


class Response:
    def __init__(self, status=0):
        self.status_code = status


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://url.com/':
        return MockResponse({"key1": "value1"}, 200)
    return MockResponse(None, 404)


class HttpHelpersTests(TestCase):
    def test_handle_status_code_no_value(self):
        response = Response()
        status = http_helpers.handle_status_code(response)
        self.assertEqual(status, 'Unknown')

    def test_handle_status_code_bad_request(self):
        response = Response(400)
        status = http_helpers.handle_status_code(response)
        self.assertEqual(status, 'Bad Request')

    def test_handle_status_code_unauthorized(self):
        response = Response(401)
        status = http_helpers.handle_status_code(response)
        self.assertEqual(status, 'Unauthorized')

    def test_handle_status_code_forbidden(self):
        response = Response(403)
        status = http_helpers.handle_status_code(response)
        self.assertEqual(status, 'Forbidden')

    def test_handle_status_code_not_found(self):
        response = Response(404)
        status = http_helpers.handle_status_code(response)
        self.assertEqual(status, 'Not Found')

    def test_handle_status_code_ok(self):
        response = Response(200)
        status = http_helpers.handle_status_code(response)
        self.assertEqual(status, 'OK')

    def test_handle_status_code_server_error(self):
        response = Response(500)
        status = http_helpers.handle_status_code(response)
        self.assertEqual(status, 'Server Error')

    def test_handle_status_code_service_unavailable(self):
        response = Response(503)
        status = http_helpers.handle_status_code(response)
        self.assertEqual(status, 'Service Unavailable')

    @mock.patch('utils.http_helpers.requests.get', side_effect=mocked_requests_get)
    def test_get_random_query(self, mock_get):
        resp = http_helpers.send_get_request('http://url.com/', headers=None)
        self.assertIn(mock.call('http://url.com/', headers=None, timeout=1), mock_get.call_args_list)
        self.assertEqual(resp.json(), {"key1": "value1"})
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
