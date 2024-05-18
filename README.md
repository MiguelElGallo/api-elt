## Setup

Clone or download [this sample's repository](https://github.com/miguelelgallo/simple-fastapi-snow-azd/), and open the `simple-fastapi-snow-azd` folder in Visual Studio Code or your preferred editor (if you're using the Azure CLI).



## Running the sample

### Testing locally

0. Create a .env file, this file should contain the following: 
(This step is mandatory, create this file before deploying to Azure)

    ```
    SNOWFLAKE_URL = youraccountidentifier
    SNOWFLAKE_USERNAME = youruser
    SNOWFLAKE_PASSWORD = yourpassword
    SNOWFLAKE_DATABASE = SNOWFLAKE_SAMPLE_DATA/TPCH_SF1
    ```

NOTE: Before moving this to production implement a Keyvault reference for your password/certificate. It is recommended to use AZURE API management to expose functions as APIs.

1. Create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate it. 
    You can name the environment .venv for example: 
    ```log
    python -m venv .venv
    ```
    This name .venv keeps the directory typically hidden in your shell and thus out of the way while giving it a name that explains why the directory exists. 
    Activate it following the instructions from the [link](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments).

NOTE: If you decide to call your virtual environment something else than .venv you need to update the value of the variable `azureFunctions.pythonVenv` to `yourname` in the `.vscode/settings.json` file.


2. Run the command below to install the necessary requirements.

    ```log
    python3 -m pip install -r requirements.txt
    ```

