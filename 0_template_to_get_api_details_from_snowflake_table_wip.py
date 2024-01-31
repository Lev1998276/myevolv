# CREATE OR REPLACE TABLE dlake.choice.api_credentials (
#     table_name VARCHAR(255),
#     api_name VARCHAR,
#     loginname VARCHAR(255),
#     password VARCHAR(255)
# );


# -- Replace the placeholder values with your actual data

# INSERT INTO dlake.choice.api_credentials (TABLE_NAME,api_name, loginname, password)
# VALUES
#     ('HOSPITALIZATION', 'https://myevolvvnshealthdev.netsmartcloud.com/api/session/authenticate', 'apiuser3', 'abc123'),
#     ('DUMMY1', 'api2', 'user2', 'password2'),
#     ('DUMMY2', 'api3', 'user3', 'password3');

import sys
import requests
import configparser
import snowflake.connector
import os
import boto3
from botocore.exceptions import ClientError
import pandas as pd
import csv
import json

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

CEDL_HOME = os.environ['CEDL_HOME']
nexus_connectionProfile = CEDL_HOME + '/etc/.sf.nexus.profile'
s3_connectionProfile = CEDL_HOME + '/etc/.s3_connection_profile'

    
def create_snowflake_connection():
    try:
        pathExist = os.path.exists(nexus_connectionProfile)
        if (not pathExist):
            print('The profile {} doesn''t exist'.format(nexus_connectionProfile))
            exit(1)
        profileFile = open(nexus_connectionProfile)
        for line in profileFile:
            if (line.split('=')[0] == 'snowflakeAccount'):
                snowflakeAccount = line.split('=')[1].replace('\n', '')
            elif (line.split('=')[0] == 'snowflakeUsername'):
                snowflakeUsername = line.split('=')[1].replace('\n', '')
            elif (line.split('=')[0] == 'snowflakePassword'):
                snowflakePassword = line.split('=')[1].replace('\n', '')
            elif (line.split('=')[0] == 'snowflakeRole'):
                snowflakeRole = line.split('=')[1].replace('\n', '')
            elif (line.split('=')[0] == 'snowflakeDBName'):
                snowflakeDBName = line.split('=')[1].replace('\n', '')
            elif (line.split('=')[0] == 'snowflakeWarehouse'):
                snowflakeWarehouse = line.split('=')[1].replace('\n', '')
            else:
                pass
        profileFile.close()
        if (len(snowflakeAccount) == 0 or len(snowflakeUsername) == 0 or len(snowflakePassword) == 0 or len(
                snowflakeRole) == 0 or len(snowflakeDBName) == 0 or len(snowflakeWarehouse) == 0):
            print('some parameters are missing from {}'.format(nexus_connectionProfile))
            exit(1)
        conn = snowflake.connector.connect(user=snowflakeUsername, password=snowflakePassword, account=snowflakeAccount,
                            warehouse=snowflakeWarehouse, database=snowflakeDBName)
        print("connected to SNOWFLAKE Database.")
    except snowflake.connector.Error as e:
        print('Error connecting to SNOWFLAKE Database - {}'.format(e))
        exit(1)
    return conn
        
def read_api_config_from_snowflake(conn, table_name):
    # Fetch API details from Snowflake table
    cursor = conn.cursor()
    cursor.execute(f"SELECT api_name, loginname, password FROM DLAKE.CHOICE.API_CREDENTIALS WHERE TABLE_NAME = '{table_name}'")
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
        print("Enter the name of the table at run time : python script.py <table_name>")
        sys.exit(1)

    table_name = sys.argv[1]
    
    sf_conn = create_snowflake_connection()

    # Fetch API details from Snowflake using the provided table name
    api_details_from_snowflake = read_api_config_from_snowflake(sf_conn,table_name)
    
    print(f"Output from the read_api_config_from_snowflake {api_details_from_snowflake}")
    
    api_url, api_user, api_password = api_details_from_snowflake[0][0],api_details_from_snowflake[0][1],api_details_from_snowflake[0][2]
    
    # Get selected API details
    print(f"Credentials to access the api are given below :-")
    print(f"api_url {api_url}")
    print(f"api_user {api_user}")
    print(f"api_password {api_password}")
    
    access_token = get_access_token(api_url, api_user, api_password)




python3 test.py HOSPITALIZATION