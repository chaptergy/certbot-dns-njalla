"""DNS Authenticator for Njalla."""
import logging

import zope.interface
from certbot import interfaces
from certbot import errors

from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon

from lexicon.providers import njalla

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Njalla

    This Authenticator uses the Njalla REST API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using Njalla for DNS)."
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=60
        )
        add("credentials", help="Njalla credentials INI file.")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the Njalla REST API."
        )

    def _setup_credentials(self):
        self._configure_file('credentials',
                             'Absolute path to Njalla credentials INI file')
        dns_common.validate_file_permissions(self.conf('credentials'))
        self.credentials = self._configure_credentials(
            "credentials",
            "Njalla credentials INI file",
            {
                "token": "Token for the Njalla API.",
            },
        )

    def _remove_subdomains(self, domain):
        split_domain = domain.split('.')
        return f'{split_domain[-2]}.{split_domain[-1]}'

    def _perform(self, domain, validation_name, validation):
        self._get_njalla_client().add_txt_record(
            self._remove_subdomains(domain), validation_name, validation
        )

    def _cleanup(self, domain, validation_name, validation):
        self._get_njalla_client().del_txt_record(
            self._remove_subdomains(domain), validation_name, validation
        )

    def _get_njalla_client(self):
        return _NjallaLexiconClient(
            self.credentials.conf("token"),
            self.ttl
        )


class _NjallaLexiconClient(dns_common_lexicon.LexiconClient):
    """
    Encapsulates all communication with the Njalla API via Lexicon.
    """

    def __init__(self, api_token, ttl):
        super(_NjallaLexiconClient, self).__init__()

        config = dns_common_lexicon.build_lexicon_config('njalla', {
            'ttl': ttl,
        }, {
            'auth_token': api_token,
        })

        self.provider = njalla.Provider(config)

    def _handle_http_error(self, e, domain_name):
        if domain_name in str(e) and (
            # 4.0 and 4.1 compatibility
            str(e).startswith('422 Client Error: Unprocessable Entity for url:') or
            # 4.2
            str(e).startswith('404 Client Error: Not Found for url:')
        ):
            return  # Expected errors when zone name guess is wrong
        return super(_NjallaLexiconClient, self)._handle_http_error(e, domain_name)
