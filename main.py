import logging
import os
from datetime import datetime, timedelta, timezone
from time import sleep

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.auth import APIKeyAuth
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_conf():
    """
    Load configuration variables from .env file.

    Returns:
        dict: A dictionary containing the loaded configuration variables.
    """
    load_dotenv()
    variables = {
        "API_URL": os.getenv("API_URL"),
        "API_KEYAUTH": os.getenv("API_KEYAUTH"),
        "API_SECRET": os.getenv("API_SECRET"),
    }
    return variables


def connect_to_api(API_URL, API_KEYAUTH, API_SECRET):
    """
    Connect to the API using the provided credentials.

    Args:
        API_URL (str): The base URL of the API.
        API_KEYAUTH (str): The name of the API key authentication.
        API_SECRET (str): The API secret key.

    Returns:
        RESTClient: An instance of the RESTClient class connected to the API.
    """
    auth = APIKeyAuth(name=API_KEYAUTH, api_key=API_SECRET, location="header")

    client = RESTClient(
        base_url=API_URL,
        auth=auth,
        paginator=PageNumberPaginator(
            base_page=1,
            page_param="page",
            maximum_page=20,
            total_path=None,
        ),  # Max set to 40
    )

    return client


def get_todays_date_twohours_ago():
    """
    Get today's date and time two hours ago.

    Returns:
        str: Today's date and time two hours ago in the format "YYYY-MM-DDTHH:MM:SS".
    """

    # In variaable now we get the current date and time in UTC
    now = datetime.now(timezone.utc)

    two_hours_ago = now - timedelta(hours=2)
    print(two_hours_ago.isoformat())
    return two_hours_ago.isoformat()


@dlt.resource(
    name="fingrid_dataset_285",
    primary_key=("startTime"),
    write_disposition="merge",
)
def fingrid_dataset_285(
    client: RESTClient,
    last_created_at=dlt.sources.incremental(
        "endTime", initial_value=get_todays_date_twohours_ago(), last_value_func=max
    ),  # Add the use of dlt.sources.incremental
    # This enables incremental loading
    # The initial value is the current date and time two hours ago
    # And then it will automatically remember the last value
):
    """
    Get data from the API using the provided RESTClient instance.

    Args:
        client (RESTClient): An instance of the RESTClient class connected to the API.
    """
    # Add the use of dlt.sources.incremental

    logger.info("get_data started")

    logger.info("Watermark is at: %s", last_created_at.start_value)

    for page in client.paginate(
        "/api/datasets/285/data",
        params={
            "pageSize": 1,
            "startTime": last_created_at.start_value,
        },  # Add the use of dlt.sources.incremental
    ):  # Note pageSize is set to 1, this is very inefficient, but it is done to show the pagination
        sleep(2)  # To avoid rate limiting
        print(page.response.json())
        if page.response.json().get("data", []) == []:
            break
        yield page.response.json().get("data", [])


def main():
    """
    The main function of the script.

    It loads the configuration, connects to the API, and downloads data from the API.
    """
    logger.info("Loading configuration from .env file.")
    config = load_conf()

    logger.info("Connecting to API.")
    logger.info("This is the base API URL: %s", config["API_URL"])
    api_client = connect_to_api(
        config["API_URL"],
        config["API_KEYAUTH"],
        config["API_SECRET"],
    )

    pipeline = dlt.pipeline(
        pipeline_name="fingrid_pipeline_dataset_285",
        destination="duckdb",
        dataset_name="fingrid_dataset_285",
    )

    load_info = pipeline.run(fingrid_dataset_285(api_client))
    logger.info("Load info: %s", load_info)


if __name__ == "__main__":
    main()
