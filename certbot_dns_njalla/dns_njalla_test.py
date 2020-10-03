"""Tests for certbot_dns_njalla.dns_njalla"""

import os
import unittest

import mock
from requests.exceptions import HTTPError

from certbot.plugins import dns_test_common
from certbot.plugins import dns_test_common_lexicon
from certbot.plugins.dns_test_common import DOMAIN

from certbot.tests import util as test_util

API_TOKEN = '0000000000000000000000000000000000000000'


class AuthenticatorTest(test_util.TempDirTestCase,
                        dns_test_common_lexicon.BaseLexiconAuthenticatorTest):

    def setUp(self):
        super(AuthenticatorTest, self).setUp()

        from certbot_dns_njalla.dns_njalla import Authenticator

        path = os.path.join(self.tempdir, 'file.ini')
        dns_test_common.write(
            {"token": API_TOKEN},
            path
        )

        print("File content: ")
        with open(path) as f:
            print(f.read())

        self.config = mock.MagicMock(njalla_credentials=path,
                                     njalla_propagation_seconds=0)  # don't wait during tests

        self.auth = Authenticator(self.config, "njalla")

        self.mock_client = mock.MagicMock()
        # _get_njalla_client | pylint: disable=protected-access
        self.auth._get_njalla_client = mock.MagicMock(
            return_value=self.mock_client)


class NjallaLexiconClientTest(unittest.TestCase,
                              dns_test_common_lexicon.BaseLexiconClientTest):
    DOMAIN_NOT_FOUND = HTTPError(
        '422 Client Error: Unprocessable Entity for url: {0}.'.format(DOMAIN))
    LOGIN_ERROR = HTTPError('401 Client Error: Unauthorized')

    def setUp(self):
        from certbot_dns_njalla.dns_njalla import _NjallaLexiconClient

        self.client = _NjallaLexiconClient(
            api_token=API_TOKEN, ttl=0)

        self.provider_mock = mock.MagicMock()
        self.client.provider = self.provider_mock


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
