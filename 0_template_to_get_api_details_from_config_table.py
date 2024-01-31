[api1]
api_name=your_api_name_1
loginname=your_login_name_1
password=your_password_1

[api2]
api_name=your_api_name_2
loginname=your_login_name_2
password=your_password_2


import sys
import requests
import json
import configparser

def get_access_token(api_name, loginname, password):
    # Rest of the function remains unchanged
    # ...

if __name__ == "__main__":
    # Check if the required command-line argument is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <config_file> <api_name>")
        sys.exit(1)

    config_file = sys.argv[1]
    selected_api_name = sys.argv[2]

    # Read configuration from the file
    config = configparser.ConfigParser()
    config.read(config_file)

    # Check if the selected API name exists in the configuration
    if selected_api_name not in config:
        print(f"API '{selected_api_name}' not found in configuration.")
        sys.exit(1)

    # Fetch API details from the configuration file
    api_name = config[selected_api_name]['api_name']
    loginname = config[selected_api_name]['loginname']
    password = config[selected_api_name]['password']

    # Get the access token
    access_token = get_access_token(api_name, loginname, password)


python script.py config.ini api1