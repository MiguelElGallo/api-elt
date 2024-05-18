from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.auth import APIKeyAuth
import logging
from dotenv import load_dotenv
import os
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_conf():
    load_dotenv()
    variables = {
        "API_URL": os.getenv("API_URL"),
        "API_KEYAUTH": os.getenv("API_KEYAUTH"),
        "API_SECRET": os.getenv("API_SECRET"),
    }
    return variables


def connect_to_api(API_URL, API_KEYAUTH, API_SECRET):
    auth = APIKeyAuth(name=API_KEYAUTH, api_key=API_SECRET, location="header")
    client = RESTClient(
        base_url=API_URL,
        auth=auth,
        paginator=PageNumberPaginator(
            initial_page=1, page_param="page", maximum_page=3, total_path=None
        ),
    )

    return client


def get_data(client: RESTClient):
    logger.info("get_data started")
    print(client.paginator)
    for page in client.paginate("/api/datasets/74/data"):
        logger.info("Page: %s", page.response.text)


def main():
    logger.info("Loading configuration from .env file.")
    config = load_conf()

    logger.info("Connecting to API.")
    logger.info("This is the base API URL: %s", config["API_URL"])
    api_client = connect_to_api(
        config["API_URL"],
        config["API_KEYAUTH"],
        config["API_SECRET"],
    )

    logger.info("Downloading data from API (paginated)")
    get_data(api_client)


if __name__ == "__main__":
    main()
