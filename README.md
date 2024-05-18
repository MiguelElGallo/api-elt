# api-elt

Fingrid API Client

This repository provides a simple Python script to call the Fingrid REST API using the dlt.sources.helpers.rest_client package. It demonstrates how to set up authentication, handle pagination, and log the responses.

## What it does

The script will:

- Load configuration variables from the `.env` file.
- Connect to the Fingrid API using the provided credentials.
- Fetch paginated data from the API endpoint `/api/datasets/74/data`.
- Log the API responses to the console.

## Code Overview

The main script consists of the following functions:

- `load_conf()`: Loads API configuration from the `.env` file.
- `connect_to_api(API_URL, API_KEYAUTH, API_SECRET)`: Sets up the `RESTClient` with API key authentication and a page number paginator.
- `get_data(client: RESTClient)`: Fetches data from the API and logs the responses.
- `main()`: Main entry point of the script, orchestrating the loading of configuration, connecting to the API, and downloading data.

## Setup

Clone or download [this sample's repository](https://github.com/MiguelElGallo/api-elt), and open the `api-elt` folder in Visual Studio Code or your preferred editor.

### Get your key

This sample uses data from Fingrid, subscribe and get your key from [Fingrid](https://data.fingrid.fi/en/instructions)

### Running the sample

### Testing locally

1. Create a .env file, this file should contain the following:

    ```env
    API_URL=https://data.fingrid.fi
    API_KEYAUTH=x-api-key
    API_SECRET=(yoursecret from the FINGRID website)
    ```

2. Create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate it.
    You can name the environment .venv for example:

    ```log
    python -m venv .venv
    ```

    This name .venv keeps the directory typically hidden in your shell and thus out of the way while giving it a name that explains why the directory exists.
    Activate it following the instructions from the [link](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments).

    NOTE: If you decide to call your virtual environment something else than .venv you need to update the value of the variable `azureFunctions.pythonVenv` to `yourname` in the `.vscode/settings.json` file.

3. Run the command below to install the necessary requirements.

    ```shell
    python3 -m pip install -r requirements.txt
    ```

4. Execute

    ```shell
    python3 main.py
    ```

### Expected output

You will set something like this:

```log
INFO:__main__:Loading configuration from .env file.
INFO:__main__:Connecting to API.
INFO:__main__:This is the base API URL: https://data.fingrid.fi
INFO:__main__:Downloading data from API (paginated)
INFO:__main__:get_data started
PageNumberPaginator at 106cac8d0: current page: 1 page_param: page total_path: None maximum_value: 3
INFO:__main__:Page: {"data":[{"datasetId":74,"startTime":"2024-05-18T11:30:00.000Z","endTime":"2024-05-18T11:45:00.000Z","value":8605.22},{"datasetId":74,"startTime":"2024-05-18T11:15:00.000Z","endTime":"2024-05-18T11:30:00.000Z","value":8571.6},{"datasetId":74,"startTime":"2024-05-18T11:00:00.000Z","endTime":"2024-05-18T11:15:00.000Z","value":8560.6},{"datasetId":74,"startTime":"2024-05-18T10:45:00.000Z","endTime":"2024-05-18T11:00:00.000Z","value":8601.05},{"datasetId":74,"startTime":"2024-05-18T10:30:00.000Z","endTime":"2024-05-18T10:45:00.000Z","value":8557.35},{"datasetId":74,"startTime":"2024-05-18T10:15:00.000Z","endTime":"2024-05-18T10:30:00.000Z","value":8584.12},{"datasetId":74,"startTime":"2024-05-18T10:00:00.000Z","endTime":"2024-05-18T10:15:00.000Z","value":8493.69},{"datasetId":74,"startTime":"2024-05-18T09:45:00.000Z","endTime":"2024-05-18T10:00:00.000Z","value":8604.88},{"datasetId":74,"startTime":"2024-05-18T09:30:00.000Z","endTime":"2024-05-18T09:45:00.000Z","value":8595.3},{"datasetId":74,"startTime":"2024-05-18T09:15:00.000Z","endTime":"2024-05-18T09:30:00.000Z","value":8632.03}],"pagination":{"total":117368,"lastPage":11737,"prevPage":null,"nextPage":2,"perPage":10,"currentPage":1,"from":0,"to":10}}
INFO:__main__:Page: {"data":[{"datasetId":74,"startTime":"2024-05-18T09:00:00.000Z","endTime":"2024-05-18T09:15:00.000Z","value":8706.88},{"datasetId":74,"startTime":"2024-05-18T08:45:00.000Z","endTime":"2024-05-18T09:00:00.000Z","value":8525.9},{"datasetId":74,"startTime":"2024-05-18T08:30:00.000Z","endTime":"2024-05-18T08:45:00.000Z","value":8510.69},{"datasetId":74,"startTime":"2024-05-18T08:15:00.000Z","endTime":"2024-05-18T08:30:00.000Z","value":8650.32},{"datasetId":74,"startTime":"2024-05-18T08:00:00.000Z","endTime":"2024-05-18T08:15:00.000Z","value":8834.53},{"datasetId":74,"startTime":"2024-05-18T07:45:00.000Z","endTime":"2024-05-18T08:00:00.000Z","value":9017.7},{"datasetId":74,"startTime":"2024-05-18T07:30:00.000Z","endTime":"2024-05-18T07:45:00.000Z","value":8954.67},{"datasetId":74,"startTime":"2024-05-18T07:15:00.000Z","endTime":"2024-05-18T07:30:00.000Z","value":8949.2},{"datasetId":74,"startTime":"2024-05-18T07:00:00.000Z","endTime":"2024-05-18T07:15:00.000Z","value":8921.84},{"datasetId":74,"startTime":"2024-05-18T06:45:00.000Z","endTime":"2024-05-18T07:00:00.000Z","value":8884.13}],"pagination":{"perPage":10,"currentPage":2,"from":10,"to":20}}
```

## Orchestrating

You can run this in Azure Batch, and trigger via Data Factory.
<https://techcommunity.microsoft.com/t5/azure-paas-blog?configure-a-simple-azure-batch-job-with-azure-data-factory/ba-p/2260759>
