#!/bin/bash

# Args:
# 1 -> name for the private key
# 2 -> name for the public key

# How to run:
# chmod +x generate-keys.sh
# source generate-keys.sh privatekey.pem publickey.pem

KEY_DIR=~/Fluid-Solutions/app/backend/epic/auth/keys

# if the directory does not exist, create it
mkdir -p "${KEY_DIR}"

# Create the private/public key pair
openssl genrsa -out "${KEY_DIR}/${1}" 2048
openssl req -new -x509 -key "${KEY_DIR}/${1}" -out "${KEY_DIR}/${2}" -subj '/CN=Fluid Solutions'


# verify the keys were created
if [ ! -f "${KEY_DIR}/${1}" ]; then
    echo "private key not created"
fi

if [ ! -f "${KEY_DIR}/${2}" ]; then
    echo "public key not created"
fi