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
    
    
#get the json data from the database     
def get_json_data(conn):
    try:
        sf_cur = sf_conn.cursor()
        query = '''
              
           SELECT 'tx_hx_hosp'     AS AutomationKey,
                   'ADD'            AS FormMode,
                   NULL             AS KeyValue,
                   D.sponsor_mrn    AS "Link to Person",
                   CASE
                     WHEN Trim(Upper(D.facility_type)) = 'HHA' THEN 'Post Acute-Home Care'
                     WHEN Trim(Upper(D.facility_type)) = 'HOSPICE' THEN 'Post Acute-Hospice'
                     WHEN Trim(Upper(D.facility_type)) = 'IRF' THEN 'Post Acute-IRF'
                     WHEN Trim(Upper(D.facility_type)) = 'LTACH' THEN
                     'Post Acute-Long Term Care'
                     WHEN Trim(Upper(D.facility_type)) = 'SNF' THEN 'Post Acute-SNF'
                     WHEN Trim(Upper(D.facility_type)) = 'HOSPITAL'
                          AND Trim(Upper(D.setting)) = 'OBSERVATION' THEN 'Observation'
                     WHEN Trim(Upper(D.facility_type)) = 'HOSPITAL'
                          AND Trim(Upper(D.setting)) = 'EMERGENCY' THEN 'ED/ER'
                     WHEN Trim(Upper(D.facility_type)) = 'HOSPITAL'
                          AND Trim(Upper(D.setting)) = 'INPATIENT' THEN 'Inpatient'
                   END              AS "Treatment History Type",
                   D.status_date
                   || ' '
                   || D.status_time AS "Admission Date",
                   NULL             AS "Discharge Date",
                   D.facility       AS "Facility Name",
                   'CAREPORT'       AS SOURCE,
                   NULL             AS Type,
                   NULL             AS Agency
            FROM   nexus.dw_owner.careport_daily_event D
            WHERE  D.sponsor_mrn = '10033814'
                   AND Trim(Upper(D.status)) NOT IN ('DISCHARGED - CANCELLED', 'ADMITTED - CANCELLED', 'SETTING CHANGED - CANCELLED' );
                    '''
        sf_cur.execute(query,)
        result = sf_cur.fetchall()
        if sf_cur.rowcount == 0:
            print('No Data available')
            exit(1)
        else:
            print("Query was executed successfully")
    except Exception as e:
        print('Error getting data from query: {}'.format(e))
        exit(1)
    return  result
    
 
#Convert data from the query to csv file 
def write_tuples_to_csv(data, file_path, header=None):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            if header:
                csv_writer.writerow(header)
            csv_writer.writerows(data)
        print(f'The data has been written to {file_path}')
    except Exception as e:
        print(f'Error writing to CSV: {e}')


def read_csv(csv_file_path):
    csv_data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Get the header from the first row
        header = next(csv_reader)
        # Iterate through rows and create dictionaries
        for row in csv_reader:
            row_dict = {header[i]: value for i, value in enumerate(row)}
            csv_data.append(row_dict)
    return csv_data




def convert_row_to_json(row):
    # Convert Admission Date to the desired format
    admission_date = datetime.strptime(row['Admission Date'], '%Y-%m-%d %I:%M %p').strftime('%m/%d/%Y %I:%M %p')

    # Extract column names dynamically
    column_names = row.keys()

    # Create FormLines based on the column names
    form_lines = [{"Caption": column, "value": row[column]} for column in column_names]

    json_data = {
        "AutomationKey": row['AutomationKey'],
        "FormMode": row['FormMode'],
        "KeyValue": row['KeyValue'],
        "FormLines": form_lines,
        "SubData": []
    }

    return json_data



def move_to_s3(local_file_path, s3_bucket_name, s3_key, archive_folder):
    try:
        # Create an S3 client
        s3 = boto3.client('s3')

        # Upload the file to the specified S3 folder
        s3.upload_file(local_file_path, s3_bucket_name, s3_key)
        print(f"File '{local_file_path}' uploaded to S3 bucket '{s3_bucket_name}' with key '{s3_key}'")

        # Archive the file with a timestamp to another S3 folder
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_key = f"{archive_folder}/{os.path.basename(local_file_path)}_{timestamp}"
        s3.upload_file(local_file_path, s3_bucket_name, archive_key)
        print(f"File archived with timestamp to S3 folder '{archive_folder}' with key '{archive_key}'")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Read the configuration
    config = read_config()
    
    # Access values from the configuration
    local_file_path = config.get('Settings', 'local_file_path')
    s3_bucket_name = config.get('Settings', 's3_bucket_name')
    s3_key = config.get('Settings', 's3_key')
    s3_archive_folder = config.get('Settings', 's3_archive_folder')
    csv_file_path = config.get('Settings', 'csv_file_path')
    output_json_file = config.get('Settings', 'output_json_file')
    
    

    #Initiate the snowflake connection
    print("Initiating the snowflake connection\n")
    sf_conn = create_snowflake_connection()


    #get the data from the Query
    print("Executing the query that gets the data set for creating json\n")
    result = get_json_data(sf_conn)
    print(f"Values returned from the function get_json_data - > {result}")


    #Writing query output to csv file 
    print("Writing query output to csv file \n")
    header_row = ['AutomationKey','FormMode','KeyValue','Link to Person','Treatment History','Admission Date','Discharge Date','Facility Name','Source','Type','Agency']
    write_tuples_to_csv(result, 'hospitalization.csv',header_row)



    # Reading the CSV data from the file to send it to json conversion
    csv_data = read_csv(csv_file_path)

    # Convert to the specified JSON structure
    # Update the KeyValue in the JSON structure
    #json_data["KeyValue"] = csv_data[0]["KeyValue"]
    print("Calling the function to create the json file structure\n")
    

    # Convert each record to JSON
    json_list = [convert_row_to_json(record) for record in csv_data]

    # Print the resulting JSON list
    for record in json_list:
        print(json.dumps(record, indent = 4))

