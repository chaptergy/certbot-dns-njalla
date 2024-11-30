"""DNS Authenticator for Njalla."""
import logging

from certbot import errors
from certbot.plugins import dns_common_lexicon

logger = logging.getLogger(__name__)


class Authenticator(dns_common_lexicon.LexiconDNSAuthenticator):
    """DNS Authenticator for Njalla

    This Authenticator uses the Njalla REST API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using Njalla for DNS)."
    ttl = 60

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._add_provider_option('token',
                                  f'Token for the Njalla API',
                                   'auth_token')

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds: int = 100) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="Njalla credentials INI file.")

    def more_info(self) -> str:
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the Njalla REST API."
        )

    @property
    def _provider_name(self) -> str:
        return 'njalla'

    def _handle_http_error(self, e, domain_name: str) -> errors.PluginError:
        # HTTP Errors are incorrectly thrown as a general error, so we need to handle both the same way
        return self._handle_all_errors(e, domain_name)

    def _handle_general_error(self, e, domain_name: str) -> errors.PluginError:
        # HTTP Errors are incorrectly thrown as a general error, so we need to handle both the same way
        return self._handle_all_errors(e, domain_name)

    def _handle_all_errors(self, e, domain_name: str) -> errors.PluginError:
        if str(e).startswith('403: Permission denied'):
            return # Expected errors when zone name guess is wrong

        hint = None
        if str(e).startswith('401:'):
            hint = 'Does your token have the right permissions?'

        hint_disp = f' ({hint})' if hint else ''

        return errors.PluginError(f'Error determining zone identifier for {domain_name}: '
                                  f'{e}.{hint_disp}')
