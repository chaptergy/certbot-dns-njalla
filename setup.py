from os import path
from setuptools import setup
from setuptools import find_packages

version = "0.0.4"

install_requires = [
    'acme>=0.31.0',
    'certbot>=0.31.0',
    'dns-lexicon>=3.4.1',
    'dnspython',
    'mock',
    'setuptools',
    'zope.interface',
    'requests'
]

# read the contents of your README file

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="certbot-dns-njalla",
    version=version,
    description="Njalla DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    repository="https://github.com/chaptergy/certbot-dns-njalla",
    author="Chaptergy",
    author_email="26956711+chaptergy@users.noreply.github.com",
    license="Apache License 2.0",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        "certbot.plugins": [
            "dns-njalla = certbot_dns_njalla.dns_njalla:Authenticator"
        ]
    },
    test_suite="certbot_dns_njalla",
)
