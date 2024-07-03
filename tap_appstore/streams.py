"""Stream type classes for tap-appstore."""

from __future__ import annotations

import sys
import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_appstore.client import AppStoreStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"


class CustomerReviews(AppStoreStream):

    name = "customerReviews"
    path = "/apps/6444049084/customerReviews"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "customerReviews.json" 

