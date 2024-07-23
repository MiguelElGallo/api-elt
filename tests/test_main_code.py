from unittest.mock import Mock

import pytest

from main import connect_to_api, get_data, get_todays_date_twohours_ago, load_conf


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("API_URL", "mock_url")
    monkeypatch.setenv("API_KEYAUTH", "mock_keyauth")
    monkeypatch.setenv("API_SECRET", "mock_secret")


@pytest.fixture
def mock_rest_client():
    return Mock()


def test_load_conf(mock_env_vars):
    config = load_conf()
    assert config["API_URL"] == "mock_url"
    assert config["API_KEYAUTH"] == "mock_keyauth"
    assert config["API_SECRET"] == "mock_secret"


def test_connect_to_api(mock_env_vars):
    client = connect_to_api("mock_url", "mock_keyauth", "mock_secret")
    assert client is not None


def test_get_todays_date_twohours_ago():
    date_str = get_todays_date_twohours_ago()
    assert isinstance(date_str, str)


def test_get_data(mock_rest_client):
    mock_rest_client.paginate.return_value = [
        Mock(
            response=Mock(
                json=Mock(
                    return_value={
                        "data": [{"startTime": "mock_time", "other_data": "mock_data"}]
                    }
                )
            )
        )
        for _ in range(2)
    ]
    data = list(get_data(mock_rest_client))
    assert data == [{"startTime": "mock_time", "other_data": "mock_data"}] * 2
