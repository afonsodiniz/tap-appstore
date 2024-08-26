"""AppStore tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_appstore import streams
from tap_appstore.appstore_streams import AppStoreBaseStream

class TapAppStore(Tap):
    """AppStore tap class."""

    name = "tap-appstore"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.appstoreconnect.apple.com/v1",
        ),
        th.Property(
            "start_date",
            th.StringType,
        ),
        th.Property(
            "app_id",
            th.StringType,
        ),
        th.Property(
            "vendor_number",
            th.StringType,
        ),
    ).to_dict()

    def discover_streams(self) -> list[AppStoreBaseStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CustomerReviews(self),
            streams.SalesReport(self)
        ]


if __name__ == "__main__":
    TapAppStore.cli()
