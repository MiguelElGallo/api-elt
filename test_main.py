from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator

from main import connect_to_api, get_data, get_todays_date_twohours_ago, load_conf


@pytest.fixture
def mock_env_variables(monkeypatch):
    monkeypatch.setenv("API_URL", "https://api.example.com")
    monkeypatch.setenv("API_KEYAUTH", "my_api_key")
    monkeypatch.setenv("API_SECRET", "my_api_secret")


def test_load_conf(mock_env_variables):
    expected_variables = {
        "API_URL": "https://api.example.com",
        "API_KEYAUTH": "my_api_key",
        "API_SECRET": "my_api_secret",
    }

    assert load_conf() == expected_variables


def test_connect_to_api(mock_env_variables):
    api_url = "https://api.example.com"
    api_keyauth = "my_api_key"
    api_secret = "my_api_secret"

    client = connect_to_api(api_url, api_keyauth, api_secret)

    assert isinstance(client, RESTClient)
    assert client.base_url == api_url
    assert client.auth.name == api_keyauth
    assert client.auth.api_key == api_secret
    assert isinstance(client.paginator, PageNumberPaginator)


def test_get_todays_date_twohours_ago():
    mock_now = datetime(2022, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    with patch("main.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        expected_date = "2021-12-31T10:00:00"
        assert get_todays_date_twohours_ago() == expected_date


def test_get_data():
    # Mock the RESTClient and its paginate method
    mock_client = MagicMock(spec=RESTClient)
    mock_paginate = MagicMock()
    mock_client.paginate = mock_paginate

    # Mock the response JSON
    mock_response_json = {
        "data": [
            {"id": 1, "name": "Data 1"},
            {"id": 2, "name": "Data 2"},
        ]
    }
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_json

    # Mock the page object
    mock_page = MagicMock()
    mock_page.response = mock_response

    # Set up the mock paginate method to yield the mock page
    mock_paginate.return_value = [mock_page]

    # Mock the start value for incremental loading
    mock_start_value = "2021-12-31T10:00:00"

    # Call the get_data function
    data_generator = get_data(mock_client, last_created_at=mock_start_value)

    # Verify the behavior
    assert list(data_generator) == [mock_response_json["data"]]
    mock_paginate.assert_called_once_with(
        "/api/datasets/74/data",
        params={"pageSize": 1, "startTime": mock_start_value},
    )


if __name__ == "__main__":
    pytest.main()
