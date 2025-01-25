#!/bin/bash

# Args:
# 1 -> name for the private key
# 2 -> name for the public key

# KEY_DIR=~/Fluid-Solutions/app/backend/Epic/keys

# # Create the private/public key pair
# openssl genrsa -out "${KEY_DIR}/${1}" 2048
# openssl req -new -x509 -key "${KEY_DIR}/${1}" -out "${KEY_DIR}/${2}" -subj '/CN=Fluid Solutions'


# # verify the keys were created
# if [ ! -f "${KEY_DIR}/${1}" ]; then
#     echo "private key not created"
# fi

# if [ ! -f "${KEY_DIR}/${2}" ]; then
#     echo "public key not created"
# fi

modulus=$(openssl x509 -noout -modulus -in ./keys/publickey.pem | sed 's/Modulus=//')
modulus_bin=$(echo -n "$modulus" | xxd -r -p)
echo -n "$modulus_bin" | base64