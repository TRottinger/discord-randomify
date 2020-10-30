import unittest
from unittest import TestCase
from utils import url_builder
import re


class UrlBuilderTests(TestCase):
    def test_url_builder_no_args(self):
        test_url = "https://my.test/url"
        built_url = url_builder.build_url(test_url)
        self.assertEqual(built_url, test_url)

    def test_url_builder_one_arg(self):
        test_url = "https://my.test/url"
        arg = "tim=best"
        built_url = url_builder.build_url(test_url, arg)
        self.assertEqual(built_url, test_url + '?' + arg)

    def test_url_builder_three_args(self):
        test_url = "https://my.test/url"
        arg1 = "one=two"
        arg2 = "a=b"
        arg3 = "square=triangle"
        built_url = url_builder.build_url(test_url, arg1, arg2, arg3)
        self.assertEqual(built_url, test_url + '?' + arg1 + '&' + arg2 + '&' + arg3)

    def test_url_builder_one_arg_badly_formed(self):
        test_url = "https://my.test/url"
        arg = "tim!worst"
        built_url = url_builder.build_url(test_url, arg)
        self.assertEqual(built_url, test_url)

    def test_url_builder_three_args_one_badly_formed(self):
        test_url = "https://my.test/url"
        arg1 = "one=two"
        arg2 = "a!b"
        arg3 = "square=triangle"
        built_url = url_builder.build_url(test_url, arg1, arg2, arg3)
        self.assertEqual(built_url, test_url + '?' + arg1 + '&' + arg3)

    def test_build_twitch_streams_url(self):
        test_url = "https://my.test/url"
        first = "1"
        game_id = "1"
        after = "1"
        built_url = url_builder.build_twitch_streams_url(test_url, first, game_id, after)
        self.assertEqual(built_url, test_url + '?first=' + first + '&game_id=' + game_id + '&after=' + after)

    def test_build_twitch_streams_url_no_cursor(self):
        test_url = "https://my.test/url"
        first = "1"
        game_id = "1"
        after = "0"
        built_url = url_builder.build_twitch_streams_url(test_url, first, game_id, after)
        self.assertEqual(built_url, test_url + '?first=' + first + '&game_id=' + game_id)

    def test_build_twitch_streams_url_bad_game(self):
        test_url = "https://my.test/url"
        first = "1"
        game_id = "0"
        after = "1"
        built_url = url_builder.build_twitch_streams_url(test_url, first, game_id, after)
        self.assertEqual(built_url, test_url + '?first=' + first + '&after=' + after)

    def test_build_twitch_streams_url_bad_game_no_cursor(self):
        test_url = "https://my.test/url"
        first = "1"
        game_id = "0"
        after = "0"
        built_url = url_builder.build_twitch_streams_url(test_url, first, game_id, after)
        self.assertEqual(built_url, test_url + '?first=' + first)


if __name__ == '__main__':
    unittest.main()
