#!/bin/bash
# Modified version of https://github.com/certbot/certbot/blob/main/tools/snap/generate_dnsplugins_snapcraft.sh
# Generate the snapcraft.yaml file for certbot-dns-njalla
# Usage: bash generate-snapcraft.sh path/to/dns/plugin
# For example, from the certbot plugin root directory:
#   generate-snapcraft.sh ./
set -e

PLUGIN_PATH=$1
PLUGIN=$(grep "^\w*name" "${PLUGIN_PATH}/pyproject.toml" | sed -E 's/[[:space:]]*name[[:space:]]*=[[:space:]]*"([^"]*)"/\1/')
DESCRIPTION=$(grep "^\w*description" "${PLUGIN_PATH}/pyproject.toml" | sed -E 's/[[:space:]]*description[[:space:]]*=[[:space:]]*"([^"]*)"/\1/')
mkdir -p "${PLUGIN_PATH}/snap"
cat <<EOF > "${PLUGIN_PATH}/snap/snapcraft.yaml"
# This file is generated automatically and should not be edited manually.
name: ${PLUGIN}
summary: ${DESCRIPTION}
description: ${DESCRIPTION}
confinement: strict
grade: stable
base: core24
adopt-info: ${PLUGIN}

parts:
  ${PLUGIN}:
    plugin: python
    source: .
    # Write the constraints from the pyproject.toml to a separate file before running craftctl
    override-pull: |
        grep -Poz '(?s)dependencies ?= ?\[\n[^\]]*\n\]' \$SNAPCRAFT_PROJECT_DIR/pyproject.toml | sed '1d;\$d' | tr -d "'\",[:blank:]" > \$SNAPCRAFT_PART_SRC/snap-constraints.txt
        craftctl default
        craftctl set version=\$(grep ^version \$SNAPCRAFT_PROJECT_DIR/pyproject.toml | cut -f2 -d= | tr -d "'\"[:space:]")
    build-environment:
      # We set this environment variable while building to try and increase the
      # stability of fetching the rust crates needed to build the cryptography
      # library.
      - CARGO_NET_GIT_FETCH_WITH_CLI: "true"
      # Constraints are passed through the environment variable PIP_CONSTRAINTS instead of using the
      # parts.[part_name].constraints option available in snapcraft.yaml when the Python plugin is
      # used. This is done to let these constraints be applied not only on the certbot package
      # build, but also on any isolated build that pip could trigger when building wheels for
      # dependencies. See https://github.com/certbot/certbot/pull/8443 for more info.
      - PIP_CONSTRAINT: \$SNAPCRAFT_PART_SRC/snap-constraints.txt
      - SNAP_BUILD: "True"
    # To build cryptography and cffi if needed
    build-packages:
      - gcc
      - git
      - build-essential
      - libssl-dev
      - libffi-dev
      - python3-dev
      - cargo
      - pkg-config
  certbot-metadata:
    plugin: dump
    source: .
    stage: [setup.py, certbot-shared]
    override-pull: |
        craftctl default
        mkdir -p \$SNAPCRAFT_PART_SRC/certbot-shared

slots:
  certbot:
    interface: content
    content: certbot-1
    read:
      - \$SNAP/lib/python3.12/site-packages

plugs:
  certbot-metadata:
    interface: content
    content: metadata-1
    target: \$SNAP/certbot-shared
EOF