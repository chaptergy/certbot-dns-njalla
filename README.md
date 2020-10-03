# Certbot plugin for authentication using Njalla

This is a plugin for [Certbot](https://certbot.eff.org/) that uses the [Njalla](https://njal.la/) API
to allow customers to prove control of a domain name.

## Usage

1. Obtain an Njalla API token (found in the [settings](https://njal.la/settings/api/))

2. Install the plugin using `pip3 install certbot-dns-njalla`, or if you are using `sudo` with certbot use `sudo -H pip3 install certbot-dns-njalla`

3. Create a `njalla.ini` config file with the following contents and apply `chmod 600 njalla.ini` on it:

   ```
   certbot_dns_njalla:dns_njalla_token=0000000000000000000000000000000000000000
   ```

   Replace the zeroes with your Njalla API key and ensure permissions are set
   to disallow access to other users.

4. Run `certbot` and direct it to use the plugin for authentication and to use
   the config file previously created:
   ```
   certbot certonly -a certbot-dns-njalla:dns-njalla --certbot-dns-njalla:dns-njalla-credentials njalla.ini -d domain.com
   ```
   Add additional options as required to specify an installation plugin etc.

## Distribution

- PyPI: https://pypi.org/project/certbot-dns-njalla/
