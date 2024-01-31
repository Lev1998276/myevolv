import sys
import requests
import json
import configparser
import snowflake.connector

def read_api_config_from_snowflake(table_name):
    # Replace the connection parameters with your Snowflake account details
    conn = snowflake.connector.connect(
        user='your_username',
        password='your_password',
        account='your_account',
        warehouse='your_warehouse',
        database='your_database',
        schema='your_schema'
    )

    # Fetch API details from Snowflake table
    cursor = conn.cursor()
    cursor.execute(f'SELECT api_name, loginname, password FROM {table_name}')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Return the API details
    return rows

def get_access_token(api_url, loginname, password):
    credentials = {
        "login_name": loginname,
        "password": password
    }

    response = requests.post(api_url, json=credentials)

    try:
        response.raise_for_status()
        
        # Check if the content type is JSON
        content_type = response.headers.get('content-type')
        if 'application/json' in content_type:
            access_token = response.json().get('access_token')
            return access_token
        elif 'text/plain' in content_type:
            # Handle text/plain response 
            text_response = response.text
            print(f"Received text/plain response: {text_response}")
            return text_response  # Return the text_response here
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
    # Check if the required command-line argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <table_name>")
        sys.exit(1)

    table_name = sys.argv[1]

    # Fetch API details from Snowflake using the provided table name
    api_details_from_snowflake = read_api_config_from_snowflake(table_name)

    # Prompt the user to select an API
    print("Select an API:")
    for i, api_detail in enumerate(api_details_from_snowflake):
        print(f"{i + 1}. {api_detail[0]}")

    selected_api_index = int(input("Enter the number corresponding to the desired API: ")) - 1

    # Get selected API details
    selected_api = api_details_from_snowflake[selected_api_index]
    api_name, loginname, password = selected_api

    # Get the access token
    access_token = get_access_token(api_name, loginname, password)




python script.py your_table_name