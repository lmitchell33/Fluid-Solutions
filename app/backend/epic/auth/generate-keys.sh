#!/bin/bash

# Args:
# 1 -> name for the private key
# 2 -> name for the public key

KEY_DIR=./keys

mkdir -p "${KEY_DIR}"
openssl genrsa -out "${KEY_DIR}/${1}" 2048
openssl req -new -x509 -key "${KEY_DIR}/${1}" -out "${KEY_DIR}/${2}" -subj '/CN=Fluid Solutions'


# verify the keys were created
if [ ! -f "${KEY_DIR}/${1}" ]; then
    echo "private key not created"
fi

if [ ! -f "${KEY_DIR}/${2}" ]; then
    echo "public key not created"
fi