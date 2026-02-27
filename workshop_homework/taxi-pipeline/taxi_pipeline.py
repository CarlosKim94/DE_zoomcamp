# ...existing code...
import requests
from typing import Iterator, Any
import dlt

BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
DEFAULT_PAGE_SIZE = 1000

@dlt.source
def taxi_source(base_url: str = BASE_URL, page_size: int = DEFAULT_PAGE_SIZE):
    """DLT source that pages through the REST API until an empty page is returned."""

    @dlt.resource(
        name="trips",
        columns={
            "rate_code": {"data_type": "bigint"},
            "mta_tax": {"data_type": "double"}
        }
    )
    def trips() -> Iterator[dict]:
        session = requests.Session()
        page = 1
        while True:
            params = {"page": page, "page_size": page_size}
            resp = session.get(base_url, params=params, timeout=30)
            resp.raise_for_status()
            page_data: Any = resp.json()
            # Expecting the endpoint to return a JSON list of records per page.
            # Stop when an empty list/page is returned.
            if not page_data:
                break
            for record in page_data:
                # ensure these fields are present and non-null so DLT can infer/types are applied
                rc = record.get("rate_code")
                if rc is None:
                    record["rate_code"] = 0
                else:
                    try:
                        record["rate_code"] = int(rc)
                    except Exception:
                        record["rate_code"] = 0

                mt = record.get("mta_tax")
                if mt is None:
                    record["mta_tax"] = 0.0
                else:
                    try:
                        record["mta_tax"] = float(mt)
                    except Exception:
                        record["mta_tax"] = 0.0

                yield record
            page += 1

    return trips

# pipeline object requested to be named `taxi_pipeline`
taxi_pipeline = dlt.pipeline(pipeline_name="taxi_pipeline", destination="duckdb")

if __name__ == "__main__":
    # example run: pipeline will pull all pages and load into the configured destination
    info = taxi_pipeline.run(taxi_source())
    print(info)
# ...existing