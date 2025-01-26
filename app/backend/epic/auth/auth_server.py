from flask import Flask, jsonify
from auth import get_public_key_modulus, kid

'''
Basic flask app to serve the JWT as required by Epic. Multiple keys can be added
to this endpoint if more than one key is required or rotation is implemented.

NOTE: I'm not actually sure if this is required becuase the token autflow works 
without it, but the documentation says it is required.
'''

app = Flask(__name__)

@app.route("/jwks", methods=["GET"])
def get_jwks():

    # Epic standard for JWT endpoints
    jwks = {
        "keys": [
            {
                "kty": "RSA",
                "alg": "RS256",
                "kid" : kid,
                "use": "sig",
                "n": f"{str(get_public_key_modulus('./keys/publickey.pem'))}",
                "e": f"AQAB"
            }
        ]
    }

    return jsonify(jwks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)