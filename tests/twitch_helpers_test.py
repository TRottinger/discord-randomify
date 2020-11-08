import os
import unittest
from unittest import TestCase, mock

import dotenv
from _pytest.monkeypatch import MonkeyPatch
import utils.twitch_helpers
from utils.twitch_helpers import TwitchHelpers
from utils import http_helpers

DUMMY_ACCESS_TOKEN = '420'


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://twitch_token_url.com/':
        return MockResponse({"key1": "value1"}, 200)
    return MockResponse(None, 404)


def mocked_get_access_token(*args):
    return DUMMY_ACCESS_TOKEN


def mocked_load_dotenv(*args):
    return


class TwitchHelpersTests(TestCase):
    def test_initialize(self):
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(utils.http_helpers, "get_access_token", mocked_get_access_token)
        twitch_helpers = TwitchHelpers(client_id='123', client_secret='456')
        self.assertEqual(twitch_helpers.client_id, '123')
        self.assertEqual(twitch_helpers.client_secret, '456')
        self.assertEqual(twitch_helpers.access_token, DUMMY_ACCESS_TOKEN)

    def test_initialize_from_env_variables(self):
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(utils.http_helpers, "get_access_token", mocked_get_access_token)
        monkeypatch.setattr(dotenv, "load_dotenv", mocked_load_dotenv)
        monkeypatch.setenv('TWITCH_CLIENT_ID', 'ENV_123')
        monkeypatch.setenv('TWITCH_CLIENT_SECRET', 'ENV_456')
        twitch_helpers = TwitchHelpers()
        self.assertEqual(twitch_helpers.client_id, 'ENV_123')
        self.assertEqual(twitch_helpers.client_secret, 'ENV_456')
        self.assertEqual(twitch_helpers.access_token, DUMMY_ACCESS_TOKEN)
