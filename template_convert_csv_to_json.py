import os
import snowflake.connector
import boto3
from botocore.exceptions import ClientError
import pandas as pd
import csv
import json
import configparser
from datetime import datetime


s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

CEDL_HOME = os.environ['CEDL_HOME']
nexus_connectionProfile = CEDL_HOME + '/etc/.sf.nexus.profile'
s3_connectionProfile = CEDL_HOME + '/etc/.s3_connection_profile'


def read_config(file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


def read_csv_from_s3(bucket_name, file_key):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Download the CSV file from S3 to a local file
    local_file = 'hospitalization.csv'
    s3.download_file(bucket_name, file_key, local_file)

    # Read the CSV file and create a list of dictionaries
    csv_data = []
    with open(local_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Get the header from the first row
        header = next(csv_reader)
        # Iterate through rows and create dictionaries
        for row in csv_reader:
            row_dict = {header[i]: value for i, value in enumerate(row)}
            csv_data.append(row_dict)
    # Clean up - remove the local copy of the CSV file
    os.remove(local_file)
    return csv_data


def convert_row_to_json(row):
    # Convert Admission Date to the desired format
    #admission_date = datetime.strptime(row['Admission Date'], '%Y-%m-%d %I:%M %p').strftime('%m/%d/%Y %I:%M %p')

    # Extract column names dynamically
    column_names = row.keys()

    # Create FormLines based on the column names
    #form_lines = [{"Caption": column, "value": row[column]} for column in column_names]
    form_lines = [{"Caption": column, "value": row[column]} for column in column_names if column not in ['AutomationKey','FormMode','KeyValue']]

    json_data = {
        "AutomationKey": row['AutomationKey'],
        "FormMode": row['FormMode'],
        "KeyValue": row['KeyValue'],
        "FormLines": form_lines,
        "SubData": []
    }
    return json_data



def list_json_files_in_folder(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.json')]
    

def upload_files_to_s3(bucket_name, local_folder, s3_folder):
    s3 = boto3.client('s3')
    json_files_to_upload = list_json_files_in_folder(local_folder)
    for file_name in json_files_to_upload:
        local_file_path = os.path.join(local_folder, file_name)
        s3_object_key = file_name
        s3.upload_file(local_file_path, bucket_name, s3_object_key)
        archive_object_key = os.path.join(s3_folder, file_name)
        s3.upload_file(local_file_path, bucket_name, archive_object_key)
        print(f"File '{file_name}' uploaded to S3.")

            
            

if __name__ == "__main__":
    # Read the configuration
    config = read_config()
    
    # Access values from the configuration
    local_file_path = config.get('Hospitalization', 'local_file_path')
    s3_bucket_name = config.get('Hospitalization', 's3_bucket_name')
    s3_key = config.get('Hospitalization', 's3_key')
    s3_folder = config.get('Hospitalization', 's3_folder')
    s3_archive_folder = config.get('Hospitalization', 's3_archive_folder')
    csv_file_path = config.get('Hospitalization', 'csv_file_path')
    json_file_path = config.get('Hospitalization', 'json_file_path')

    csv_data = read_csv_from_s3(s3_bucket_name, s3_key)

    # Display the CSV data
    for row in csv_data:
        print(row)

    # Convert each csv record to JSON
    json_list = [convert_row_to_json(record) for record in csv_data]

    # Print the resulting JSON list
    counter = 1  # Initialize a counter

    for record in json_list:
        key_value = record["KeyValue"]
        date_str = datetime.now().strftime("%Y%m%d")  
        file_name = f"record_{key_value}_{date_str}_{counter}.json"
        counter += 1
        # Modify the file path to include the output directory
        file_path = os.path.join(json_file_path, file_name)
        with open(file_path, "w") as json_file:
            json.dump(record, json_file, indent=2)
        print(f"JSON file dumped successfully at {file_path}")
