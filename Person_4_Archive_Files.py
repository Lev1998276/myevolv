import os
import shutil
import configparser
from datetime import datetime



def read_config(file_path='config_person.ini'):
    try:
        config = configparser.ConfigParser()
        config.read(file_path)
        return config
    except Exception as e:
        print(f"An error occurred while reading the configuration file: {e}")
    

def archive_files(source_dir, destination_dir):
    try:
        # Ensure source directory exists
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

        # Ensure destination directory exists, create if not
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

        for file_name in files:
            source_path = os.path.join(source_dir, file_name)
            
            # Add a timestamp to the file name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            destination_file_name = f"{file_name}_{timestamp}"

            destination_path = os.path.join(destination_dir, destination_file_name)

            shutil.move(source_path, destination_path)
            print(f"Archived: {file_name} as {destination_file_name}")

        print(f"All files archived from '{source_dir}' to '{destination_dir}' with timestamps.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
        
def add_timestamps_to_files(folder_path, filename):
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        old_path = os.path.join(folder_path, filename)
        file_name, file_extension = os.path.splitext(filename)
        new_file_name = f"{current_time}_{file_name}{file_extension}"
        new_path = os.path.join(folder_path, new_file_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} to {new_file_name}")

    except Exception as e:
        print(f"An error occurred for file {filename}: {e}")


if __name__ == "__main__":

    # Read the configuration
    config = read_config()
    
    csv_file_path = config.get('Person', 'csv_file_path')
    csv_archive_file_path = config.get('Person', 'csv_archive_file_path')
    json_file_path = config.get('Person', 'json_file_path')
    json_archive_file_path = config.get('Person', 'json_archive_file_path')
    error_file_path = config.get('Person', 'error_file')
    log_file_path = config.get('Person', 'log_file')
    posted_file_path = config.get('Person', 'posted_json') 

    ##archive json files
    json_source_directory = json_file_path
    json_destination_directory = json_archive_file_path
    archive_files(json_source_directory, json_destination_directory)
    
    #archive csv  files
    csv_source_directory = csv_file_path
    csv_destination_directory = csv_archive_file_path
    archive_files(csv_source_directory, csv_destination_directory)
    
    #adding timestamps to posted , error and log files 
    add_timestamps_to_files(error_file_path, 'error_records.txt')
    add_timestamps_to_files(log_file_path, 'log_records.txt')
    add_timestamps_to_files(posted_file_path,'posted_records.txt')
    

