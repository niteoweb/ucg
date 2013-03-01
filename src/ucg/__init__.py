#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import socket
import phpserialize

from ucg import exceptions as ex
from time import sleep


class UCG(object):
    """A class representing the UCG API
    (http://www.generateuniquecontent.com/api.php).
    All articles must be in UTF-8 encoding!
    """

    """URLs for invoking the API"""
    URL = 'http://uc.apnicservers.com/uc-api/api_v1.php'

    TIMEOUT = 20

    DEFAULT_PARAMS = [
        ["NN", "noun", "similar", 0],
        ["VBD", "verb", "synonym", 1],
        ["VBG", "verb", "synonym", 1],
        ["VBN", "verb", "synonym", 1],
        ["VB", "verb", "synonym", 0],
        ["JJ", "adjective", "similar", 0],
        ["RB", "adverb", "similar", 0]
    ]

    def __init__(self, email, apikey):
        """Initializes the spin api object.

        :param email: login email address
        :type email: str
        :param password: key to access api
        :type password: str
        """
        self._email = email
        self._apikey = apikey

    def _send_request(self, args):
        """ Invoke UCG API with given parameters and return its response.

        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: API's response
        :rtype: dict
        """
        data = "function={0}".format(args[0])

        for i in range(1, len(args)):
            data += "&uc_param{0}={1}".format(
                i,
                urllib.quote_plus(phpserialize.dumps(args[i]))
            )

        print data

        try:
            response = urllib2.urlopen(
                self.URL,
                data=data,
                timeout=self.TIMEOUT
            )
        except socket.timeout as e:
            raise ex.NetworkError(str(e))

        result = response.read()

        if result == "-20":
            raise ex.ProcessError("Invalid/bad function call")

        return result

    def login(self):
        result = self._send_request([
            "login", self._apikey, self._email
        ])
        if result == "0":
            raise ex.AuthenticationError("could not log in")
        self._session_key = result
        return result

    def logout(self):
        result = self._send_request([
            "clean", self._session_key
        ])
        return result

    def get_credits(self):
        result = self._send_request([
            "getCredits", self._session_key
        ])
        if result == "-10":
            raise ex.AuthenticationError("user not logged in")
        return result

    def _add_queue(self, text, params=None, super=1, replace_caps=False):
        result = self._send_request([
            "addQueue",
            self._session_key,
            text,
            self.DEFAULT_PARAMS,
            super,
            1 if replace_caps else 0
        ])
        if result == "-10":
            raise ex.AuthenticationError("user not logged in")
        elif result == "-11":
            raise ex.ArgumentError("missing/bad arguments")
        elif result == "-12":
            raise ex.SpinError("text is too long, maximum 10k characters")
        elif result == "-13":
            raise ex.QuotaError("no credits remaining")
        return result

    def _get_queue(self, qid):
        result = self._send_request([
            "getQueue",
            self._session_key,
            qid
        ])
        if result == "-10":
            raise ex.AuthenticationError("user not logged in")
        elif result == "-11":
            raise ex.ArgumentError("no arguments")
        elif result == "-12":
            raise ex.ArgumentError("invalid arguments")
        elif result == "-13":
            raise ex.QueueError("bad queue id")
        elif result == "-14":
            raise ex.QueueError("no such queue id")
        elif result == "-15":
            raise ex.NotReadyError("item not ready yet (qid: {0})".format(qid))
        elif result == "-16":
            raise ex.ProcessError("credit refund issued, could not process")
        return result

    def text_with_spintax(self):
        raise NotImplemented()

    def unique_variation(self, text, params=None, wait=True):
        """ Return a unique variation of the given text.

        :param text: original text that needs to be changed
        :type text: string
        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: processed text
        :rtype: string
        """
        qid = self._add_queue(text, params)

        while True:
            try:
                result = self._get_queue(qid)
            except ex.NotReadyError as e:
                print str(e)
                if wait:
                    sleep(5)
                    continue
                else:
                    raise e
            return result
