#!/bin/bash

# Install Knative Function (func)
curl -sL https://github.com/knative/func/releases/latest/download/func_linux_amd64 --output func
chmod +x func
sudo mv func /usr/local/bin/