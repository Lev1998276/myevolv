import os
import shutil
import configparser
from datetime import datetime



def read_config(file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config
    


def archive_files(source_dir, destination_dir):
    try:
        # Ensure source directory exists
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

        # Ensure destination directory exists, create if not
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Get a list of all files in the source directory
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

        # Move each file to the destination directory with a timestamp
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

if __name__ == "__main__":

    # Read the configuration
    config = read_config()
    
    csv_file_path = config.get('Hospitalization', 'csv_file_path')
    csv_archive_file_path = config.get('Hospitalization', 'csv_archive_file_path')
    json_file_path = config.get('Hospitalization', 'json_file_path')
    json_archive_file_path = config.get('Hospitalization', 'json_archive_file_path')

    json_source_directory = json_file_path
    json_destination_directory = json_archive_file_path

    archive_files(json_source_directory, json_destination_directory)

    csv_source_directory = csv_file_path
    csv_destination_directory = csv_archive_file_path

    archive_files(csv_source_directory, csv_destination_directory)

