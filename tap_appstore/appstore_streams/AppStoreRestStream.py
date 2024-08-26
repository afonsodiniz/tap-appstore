from .AppStoreBaseStream import AppStoreBaseStream
import requests
from typing import Any, Iterable

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from singer_sdk.helpers.jsonpath import extract_jsonpath

class AppStoreRestStream(AppStoreBaseStream):

    next_page_token_jsonpath = "$.next_page"
    records_jsonpath = "$.data[*]"

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        yield from extract_jsonpath(self.records_jsonpath, input=response.json())
