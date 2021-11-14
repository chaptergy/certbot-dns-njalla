# Certbot plugin for authentication using Njalla

This is a plugin for [Certbot](https://certbot.eff.org/) that uses the [Njalla](https://njal.la/) API
to allow customers to prove control of a domain name.

## Usage

1. Obtain an Njalla API token (found in the [settings](https://njal.la/settings/api/))

2. Install the plugin using `pip3 install certbot-dns-njalla`, or if you are using `sudo` with certbot use `sudo -H pip3 install certbot-dns-njalla`

3. Create a `njalla.ini` config file with the following contents and apply `chmod 600 njalla.ini` on it:

   ```ini
   dns_njalla_token=<token>
   ```

   Replace `<token>` with your Njalla API key and ensure permissions are set
   to disallow access to other users.

4. Run `certbot` and direct it to use the plugin for authentication and to use
   the config file previously created:
   ```sh
   certbot -a dns-njalla --dns-njalla-credentials njalla.ini -d domain.com
   ```
   Use `*.domain.com` if you want to generate it as a wildcard certificate.  
   Add additional options as required to specify an installation plugin etc.

## Development

### Install local files as python package

Run the following command replacing `<path>` with the path to the folder containing the `setup.py` file (`./` when in repository root):

```sh
pip3 install -e <path>
```

### Run tests

Execute the following command inside the root-directory

```sh
python -m unittest discover -p '*_test.py'
```

## Distribution

- PyPI: https://pypi.org/project/certbot-dns-njalla/
