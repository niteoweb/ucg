# -*- coding: utf-8 -*-

from ucg import UCG
from ucg import exceptions as ex

import mock
import unittest2 as unittest
import socket


class TestApi(unittest.TestCase):

    def setUp(self):
        """Utility code shared among all tests."""
        self.ucg = UCG('foo@bar.com', 'apikey')
        self.ucg._session_key = '1234-567890-1234'

    def test_init(self):
        """Test initialization of UCG.

        UCG is initialized on every test run and stored as self.ucg.
        We need to test for stored values if class was
        initialized correctly.
        """
        self.assertIsInstance(self.ucg, UCG)
        self.assertEquals(self.ucg._email, 'foo@bar.com')
        self.assertEquals(
            self.ucg._apikey,
            'apikey'
        )

    def test_url(self):
        """Test UCG API URL"""
        self.assertEquals(
            UCG.URL,
            "http://uc.apnicservers.com/uc-api/api_v1.php"
        )

    def test_default_params(self):
        """Test default parameters"""
        self.assertEquals(
            UCG.DEFAULT_PARAMS,
            [
                ["NN", "noun", "similar", 0],
                ["VBD", "verb", "synonym", 1],
                ["VBG", "verb", "synonym", 1],
                ["VBN", "verb", "synonym", 1],
                ["VB", "verb", "synonym", 0],
                ["JJ", "adjective", "similar", 0],
                ["RB", "adverb", "similar", 0]
            ]
        )

    @mock.patch('ucg.urllib2')
    def test_unique_variation_call(self, urllib2):
        """Test call of unique_variation() with default values."""
        # mock response from UCG
        mocked_response = "Some evaluation text whič is fü."
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # test call
        self.assertEquals(
            self.ucg.unique_variation(u"Some test text whič is fü."),
            u"Some evaluation text whič is fü.",
        )

    @mock.patch('ucg.urllib2')
    def test_unique_variation_script_call(self, urllib2):
        """Test call of unique_variation() with default values."""
        # mock response from UCG
        mocked_response = ('Some big cookie to whirl.<script type="text/'
                           'javascript" src="http://www.generateuniquecontent'
                           '.com/js/ucg.js\?qid=ABCDEF"></script>')
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # test call
        self.assertEquals(
            self.ucg.unique_variation(u"Some long text to spin."),
            u"Some big cookie to whirl.",
        )

    @mock.patch('ucg.urllib2')
    def test_exception_timeout(self, mocked_urllib2):
        """Test timeout error."""
        # set side effect
        mocked_urllib2.urlopen.side_effect = socket.timeout("timeout foo")

        # test call
        self.assertRaises(
            ex.NetworkError,
            self.ucg.unique_variation,
            u"Some test text whič is fü."
        )

    @mock.patch('ucg.urllib2')
    def test_text_with_spintax(self, mocked_urllib2):
        """Test call of text_with_spintax(), it is not yet implemented."""
        self.assertRaises(
            ex.NotImplementedError,
            self.ucg.text_with_spintax
        )
