#!/bin/bash

set -e

LAZYDOCKER_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazydocker/releases/latest" | grep -Po '"tag_name": "v\K[0-9.]+')

curl -Lo /tmp/lazydocker.tar.gz "https://github.com/jesseduffield/lazydocker/releases/latest/download/lazydocker_${LAZYDOCKER_VERSION}_Linux_x86_64.tar.gz"

mkdir /tmp/lazydocker
tar -xf /tmp/lazydocker.tar.gz -C /tmp/lazydocker

sudo mv /tmp/lazydocker/lazydocker /usr/local/bin

lazydocker --version
rm -rf /tmp/lazydocker.tar.gz /tmp/lazydocker
