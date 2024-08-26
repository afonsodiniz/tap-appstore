"""REST client handling, including AppStoreStream base class."""

from __future__ import annotations

import jwt
from datetime import datetime, timedelta

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.streams import RESTStream
import sys
import os
import base64

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

class AppStoreBaseStream(RESTStream):


    @property
    def generate_jwt_token(self) -> str:

        encoded_key = os.environ.get('TAP_APPSTORE_PRIVATE_KEY')

        if encoded_key is None:
            raise ValueError("An error has occured with the Encoded Key.")

        private_key = base64.b64decode(encoded_key).decode('utf-8')
    

        current_local_time = datetime.utcnow() # + timedelta(hours=1) # uncomment if locally testing
        expiration_time = current_local_time + timedelta(minutes=10)

        iat = int(current_local_time.timestamp())
        exp = int(expiration_time.timestamp())

        # Set JWT headers and payload
        header = {
            "alg": "ES256",         
            "kid": "VVTRQ82P72",
            "typ": "JWT"
        }

        payload = {
            "iss": "986c6837-b835-41cc-8b1e-cfc9e3853f4f",
            "iat": iat,
            "exp": exp,
            "aud": "appstoreconnect-v1"
        }

        encoded_jwt = jwt.encode(payload, private_key, algorithm='ES256', headers=header)

        return encoded_jwt
    
    @property
    def url_base(self) -> str:

        return self.config.get("api_url")

    @property
    def authenticator(self) -> BearerTokenAuthenticator:

        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.generate_jwt_token
        )
