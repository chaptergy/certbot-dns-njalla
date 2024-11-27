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
                        dns_test_common_lexicon.BaseLexiconDNSAuthenticatorTest):

    DOMAIN_NOT_FOUND = HTTPError('422 Client Error: Unprocessable Entity for url: {0}.'.format(DOMAIN))
    LOGIN_ERROR = HTTPError('401 Client Error: Unauthorized')

    def setUp(self):
        super().setUp()

        from certbot_dns_njalla.dns_njalla import Authenticator

        path = os.path.join(self.tempdir, 'file.ini')
        dns_test_common.write(
            {"njalla_token": API_TOKEN},
            path
        )

        # print("File content: ")
        # with open(path) as f:
        #     print(f.read())

        self.config = mock.MagicMock(njalla_credentials=path,
                                     njalla_propagation_seconds=0)  # don't wait during tests

        self.auth = Authenticator(self.config, "njalla")

if __name__ == "__main__":
    unittest.main()  # pragma: no cover
