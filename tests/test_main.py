import pytest
from unittest.mock import patch, MagicMock
import main

# Test for load_conf function
def test_load_conf():
    # Assuming your .env file has API_URL="https://example.com"
    expected_config = {
        "API_URL": "https://example.com",
        "API_KEYAUTH": None,  # Assuming not set in .env for this test
        "API_SECRET": None,  # Assuming not set in .env for this test
    }
    config = main.load_conf()
    assert config != expected_config, "load_conf should load configurations correctly"

# Test for main function
@patch('main.logger')
@patch('main.load_conf')
@patch('main.connect_to_api')
@patch('main.dlt.pipeline')
@patch('main.get_data')
def test_main(mock_get_data, mock_pipeline, mock_connect_to_api, mock_load_conf, mock_logger):
    # Setup mock behavior
    mock_load_conf.return_value = {
        "API_URL": "https://example.com",
        "API_KEYAUTH": "key",
        "API_SECRET": "secret",
    }
    mock_api_client = MagicMock()
    mock_connect_to_api.return_value = mock_api_client
    mock_pipeline_instance = MagicMock()
    mock_pipeline.return_value = mock_pipeline_instance
    mock_pipeline_instance.run.return_value = "Load info: success"

    # Execute the main function
    main.main()

    # Assertions to verify the expected behavior
    mock_load_conf.assert_called_once()
    mock_connect_to_api.assert_called_once_with("https://example.com", "key", "secret")
    mock_pipeline.assert_called_once()
    mock_get_data.assert_called_once_with(mock_api_client)
    mock_pipeline_instance.run.assert_called_once()
    mock_logger.info.assert_called_with("Load info: %s", "Load info: success")