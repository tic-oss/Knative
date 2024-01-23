#!/bin/bash

# Download and install the Knative CLI (kn)
curl -sL https://github.com/knative/client/releases/latest/download/kn-linux-amd64 --output kn
chmod +x kn
sudo mv kn /usr/local/bin/