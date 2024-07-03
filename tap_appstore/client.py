"""REST client handling, including AppStoreStream base class."""

from __future__ import annotations

import sys
from typing import Any, Callable, Iterable
import jwt
from datetime import datetime, timedelta

import requests
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream
import base64

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources
import os

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]

SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"


class AppStoreStream(RESTStream):

    records_jsonpath = "$.data[*]"  
    next_page_token_jsonpath = "$.next_page" 

    @property
    def generate_jwt_token(self) -> str:

        encoded_key = os.environ.get('TAP_APPSTORE_PRIVATE_KEY')

        if encoded_key is None:
            raise ValueError("An error has occured with the Encoded Key.")

        private_key = base64.b64decode(encoded_key).decode('utf-8')
    

        current_local_time = datetime.utcnow() + timedelta(hours=1) 
        expiration_time = current_local_time + timedelta(minutes=10)

        iat = int(current_local_time.timestamp())
        exp = int(expiration_time.timestamp())

        # Set JWT headers and payload
        header = {
            "alg": "ES256",         
            "kid": "PY8HN4AUCX",
            "typ": "JWT"
        }

        payload = {
            "iss": "986c6837-b835-41cc-8b1e-cfc9e3853f4f",
            "iat": iat,
            "exp": exp,
            "aud": "appstoreconnect-v1"
        }

        print(payload)
        encoded_jwt = jwt.encode(payload, private_key, algorithm='ES256', headers=header)
        print(encoded_jwt)

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

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.
        return row
