# Certbot plugin for authentication using Njalla

This is a plugin for [Certbot](https://certbot.eff.org/) that uses the [Njalla](https://njal.la/) API
to allow customers to prove control of a domain name.

## Installation

### Python / pip

Use this method if you have also installed `certbot` via `pip`.
Install the plugin using

```commandline
pip3 install certbot-dns-njalla
```

If you are using `sudo` with certbot use `sudo -H pip3 install certbot-dns-njalla` instead.

### Snap

Use this method if you have also installed `certbot` via `snap`.

```commandline
snap install certbot-dns-njalla
```

Now connect the certbot installation with the njalla plugin installation.

```commandline
sudo snap connect certbot:plugin certbot-dns-njalla
```

## Usage

1. Make sure the plugin is installed and connected. You can verify this by running `certbot plugins`. `dns-njalla` should be in the list.

2. Obtain an Njalla API token (found in the [settings](https://njal.la/settings/api/))

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

   Remember to use the `-i` flag if you want to use an additional installer plugin, like `-i apache` or `-i nginx`.

## Development

### Install local files as python package

Run the following command in the repository root (so you are in the folder containing the `setup.py`):

```sh
pip3 install -e ./
```

### Build snap locally

By default a snap is built automatically by snapcraft if there are changes in the git repo. But here is what to do to test the build locally.

Do the basic setup described in the [certbot snap readme](https://github.com/certbot/certbot/tree/master/tools/snap#local-testing-and-development). (Mainly installing setting up lxd)
Run the following command in the repository root (so you are in the folder containing the `setup.py`):

```sh
sh generate_dnsplugins_snapcraft.sh
snapcraft clean --use-lxd
snapcraft --debug --use-lxd
```

### Run tests

Execute the following command inside the root-directory

```sh
python -m unittest discover -p '*_test.py'
```

## Distribution

- PyPI: https://pypi.org/project/certbot-dns-njalla/
