[HOSPITALIZATION]
api_name=https://myevolvvnshealthdev.netsmartcloud.com/api/session/authenticate
loginname=apiuser3
password=abc123

[api2]
api_name=your_api_name_2
loginname=your_login_name_2
password=your_password_2


import sys
import requests
import json
import configparser

def get_access_token(api_url, loginname, password):
    credentials = {
        "login_name": loginname,
        "password": password
    }
    response = requests.post(api_url, json=credentials)
    try:
        response.raise_for_status()
        content_type = response.headers.get('content-type')
        if 'application/json' in content_type:
            access_token = response.json().get('access_token')
            return access_token
        elif 'text/plain' in content_type:
            text_response = response.text
            print(f"Received text/plain response: {text_response}")
            return text_response  
        else:
            print(f"Unexpected content type: {content_type}. Unable to handle response.")
            return None
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
    print(f"Authentication failed. Status code: {response.status_code}")
    return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <config_file> <api_name>")
        sys.exit(1)

    config_file = sys.argv[1]
    selected_api_name = sys.argv[2]


    print("Hello")
    # Read configuration from the file
    config = configparser.ConfigParser()
    config.read(config_file)

    # Check if the selected API name exists in the configuration
    if selected_api_name not in config:
        print(f"API '{selected_api_name}' not found in configuration.")
        sys.exit(1)

    print("Hello")
    
    # Fetch API details from the configuration file
    api_name = config[selected_api_name]['api_name']
    loginname = config[selected_api_name]['loginname']
    password = config[selected_api_name]['password']
    
    print("Hello")

    # Get the access token
    access_token = get_access_token(api_name, loginname, password)



# ATTENTION : USE THE FOLLOIWNG TO RUN THE PROGRAM
python3 test.py config_api.ini HOSPITALIZATION