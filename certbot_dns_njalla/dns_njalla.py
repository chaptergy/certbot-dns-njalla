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
        hint = None
        if str(e).startswith('401 Client Error: Unauthorized for url:'):
            hint = 'Is your API token value correct?'

        hint_disp = f' ({hint})' if hint else ''

        return errors.PluginError(f'Error determining zone identifier for {domain_name}: '
                                  f'{e}.{hint_disp}')
