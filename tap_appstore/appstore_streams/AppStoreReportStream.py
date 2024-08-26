
from .AppStoreBaseStream import AppStoreBaseStream
import requests
from typing import Any, Callable, Iterable

import gzip
import json
from io import BytesIO, StringIO
import csv

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AppStoreReportStream(AppStoreBaseStream):
    
    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """
        Parse the response and return an iterator of result records.
        Handles gzipped content if detected in the response headers.
        """

        with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
            decompressed_data = gz.read().decode('utf-8')

            csv_file = StringIO(decompressed_data)
            csv_reader = csv.DictReader(csv_file, delimiter='\t') 

            for row in csv_reader:

                transformed_row = {field.lower().replace(' ', '_'): value.strip() for field, value in row.items()}
                yield transformed_row
