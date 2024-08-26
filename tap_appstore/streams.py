"""Stream type classes for tap-appstore."""

from __future__ import annotations

import sys
import typing as t
import os

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_appstore.appstore_streams import AppStoreReportStream, AppStoreRestStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"

APP_ID = os.getenv('TAP_APPSTORE_APP_ID')
VENDOR_NUMBER = os.getenv('TAP_APPSTORE_VENDOR_NUMBER')

class CustomerReviews(AppStoreRestStream):

    name = "customerReviews"
    path = f"/apps/{APP_ID}/customerReviews"
    primary_keys = ["id"]
    schema_filepath = SCHEMAS_DIR / "customerReviews.json"


class SalesReport(AppStoreReportStream):

    name = "salesReport"
    path = f"/salesReports?filter[reportType]=SALES&filter[reportSubType]=SUMMARY&filter[frequency]=DAILY&filter[vendorNumber]={VENDOR_NUMBER}"
    schema_filepath = SCHEMAS_DIR / "salesReport.json"

