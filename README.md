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

5. Execute as Github Action

To execute this code in a GitHub Actions runner, you can create a workflow file in your repository, see `.github/workflows/etlinrunner.yml`. You can see the executions also from this repository.

***Note:*** As a GitHub action, the execution will create a duckdb file that will be created in the runner, after the runner finishes you will loose the file. You can add Python/DuckdDB code to create that file in Cloud Storage like Azure Data Lake, S3, etc. You will need to deal with authentication.

### Incremental load

Now it has support for incremental load, as you can see in this code:

```python
def get_data(
    client: RESTClient,
    last_created_at=dlt.sources.incremental(
        "startTime", initial_value=get_todays_date_twohours_ago(), last_value_func=max
    ),  # Add the use of dlt.sources.incremental
    # This enables incremental loading
    # The initial value is the current date and time two hours ago
    # And then it will automatically remember the last value
):
```

The first time it starts to load from the current time minus two hours. Then it will set the watermark to the last record loaded. After that only two delta or incremental will happen, everything handled for your automatically.

### Checking the loads

You can run this command:

```shell
duckdb fingrid_pipeline_dataset_74.duckdb
```

You will enter the DuckDB prompt, then execute the different sql statements:

```log
 select * from fingrid_dataset_74.get_data;
┌────────────┬──────────────────────────┬──────────────────────────┬─────────┬────────────────────┬────────────────┐
│ dataset_id │        start_time        │         end_time         │  value  │    _dlt_load_id    │    _dlt_id     │
│   int64    │ timestamp with time zone │ timestamp with time zone │ double  │      varchar       │    varchar     │
├────────────┼──────────────────────────┼──────────────────────────┼─────────┼────────────────────┼────────────────┤
│         74 │ 2024-05-25 18:30:00+03   │ 2024-05-25 18:45:00+03   │ 7344.87 │ 1716653382.9283059 │ ONxkQ/7htjAyLw │
│         74 │ 2024-05-25 18:15:00+03   │ 2024-05-25 18:30:00+03   │ 7328.06 │ 1716653382.9283059 │ VaMdhU9TnXFanA │
│         74 │ 2024-05-25 18:00:00+03   │ 2024-05-25 18:15:00+03   │ 7377.55 │ 1716653382.9283059 │ aL2dod+gbSHopw │
│         74 │ 2024-05-25 17:45:00+03   │ 2024-05-25 18:00:00+03   │  7297.2 │ 1716653382.9283059 │ +1MHPgU2onPYoQ │
│         74 │ 2024-05-25 17:30:00+03   │ 2024-05-25 17:45:00+03   │ 7258.52 │ 1716653382.9283059 │ Uo2qq66VwJmmRQ │
│         74 │ 2024-05-25 17:15:00+03   │ 2024-05-25 17:30:00+03   │ 7380.26 │ 1716653382.9283059 │ lXwFJcTr9lnqWQ │
│         74 │ 2024-05-25 20:30:00+03   │ 2024-05-25 20:45:00+03   │ 7030.78 │ 1716660587.4837272 │ ALh5osQYJ1EuaQ │
│         74 │ 2024-05-25 20:15:00+03   │ 2024-05-25 20:30:00+03   │ 6979.95 │ 1716660587.4837272 │ Hpx71+1c6E1u4Q │
│         74 │ 2024-05-25 20:00:00+03   │ 2024-05-25 20:15:00+03   │ 7050.27 │ 1716660587.4837272 │ /DEYqg2PubVO2g │
│         74 │ 2024-05-25 19:45:00+03   │ 2024-05-25 20:00:00+03   │ 7109.54 │ 1716660587.4837272 │ 0xPAcUmSVdlpFA │
│         74 │ 2024-05-25 19:30:00+03   │ 2024-05-25 19:45:00+03   │  7145.4 │ 1716660587.4837272 │ x2Icixjf98GnKA │
│         74 │ 2024-05-25 19:15:00+03   │ 2024-05-25 19:30:00+03   │ 7132.35 │ 1716660587.4837272 │ HyqCdz90sd/PtA │
│         74 │ 2024-05-25 19:00:00+03   │ 2024-05-25 19:15:00+03   │ 7237.78 │ 1716660587.4837272 │ 0axTFaX8NE0Hcw │
│         74 │ 2024-05-25 18:45:00+03   │ 2024-05-25 19:00:00+03   │ 7363.15 │ 1716660587.4837272 │ nVGm0Pz1E7Ab1w │
├────────────┴──────────────────────────┴──────────────────────────┴─────────┴────────────────────┴────────────────┤
│ 14 rows                                                                                                6 columns │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

You can see in column ```_dlt_load_id``` two values, because I executed the load, then waited some hours and loaded again, where it fetched delta records. The delta records start in line 7 where```_dlt_load_id``` changes to ```1716660587.483727```.

There is also metada available,execute the following command:
```log

select * from fingrid_dataset_74._dlt_loads;
┌────────────────────┬─────────────────────────────┬────────┬───────────────────────────────┬──────────────────────────────────────────────┐
│      load_id       │         schema_name         │ status │          inserted_at          │             schema_version_hash              │
│      varchar       │           varchar           │ int64  │   timestamp with time zone    │                   varchar                    │
├────────────────────┼─────────────────────────────┼────────┼───────────────────────────────┼──────────────────────────────────────────────┤
│ 1716653382.9283059 │ fingrid_pipeline_dataset_74 │      0 │ 2024-05-25 19:10:09.155099+03 │ QdD7VXojMsfePT3mgQTCDKRxUjOqAwIWYyqHPd7BrMI= │
│ 1716660587.4837272 │ fingrid_pipeline_dataset_74 │      0 │ 2024-05-25 21:10:53.835926+03 │ QdD7VXojMsfePT3mgQTCDKRxUjOqAwIWYyqHPd7BrMI= │
└────────────────────┴─────────────────────────────┴────────┴───────────────────────────────┴──────────────────────────────────────────────┘
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
