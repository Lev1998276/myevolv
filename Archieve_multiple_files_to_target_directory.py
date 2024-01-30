# archive multiple files to a target directory

import os
import zipfile
from datetime import datetime
import glob

def archive_files_with_timestamp(directory_path, file_pattern, target_directory):
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Find files that match the specified pattern in the directory
    files_to_archive = glob.glob(os.path.join(directory_path, file_pattern))

    for file_path in files_to_archive:
        # Extract the file's base name and extension
        base_name, extension = os.path.splitext(os.path.basename(file_path))

        # Create a new filename with the timestamp
        archived_filename = f"{base_name}_{timestamp}{extension}"

        # Create the full path for the zip archive in the target directory
        target_path = os.path.join(target_directory, archived_filename)

        # Create a zip archive with the timestamped filename in the target directory
        with zipfile.ZipFile(target_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.write(file_path, os.path.basename(file_path))

        print(f'File archived with timestamp: {target_path}')

# Example usage:
directory_to_archive = '/AppDev/CEDL/etl/SrcFiles/lg/visit'
file_pattern_to_match  = 'output*.csv'
target_archive_directory = '/AppDev/CEDL/etl/SrcFiles/lg/visit/archive'

archive_files_with_timestamp(directory_to_archive, file_pattern_to_match, target_archive_directory)




#####################################################################################
import os
import zipfile
from datetime import datetime
import glob

def archive_files_with_timestamp(directory_path, file_pattern):
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Find files that match the specified pattern in the directory
    files_to_archive = glob.glob(os.path.join(directory_path, file_pattern))

    for file_path in files_to_archive:
        # Extract the file's base name and extension
        base_name, extension = os.path.splitext(os.path.basename(file_path))

        # Create a new filename with the timestamp
        archived_filename = f"{base_name}_{timestamp}{extension}"

        # Create a zip archive with the timestamped filename
        with zipfile.ZipFile(archived_filename, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.write(file_path, os.path.basename(file_path))

        print(f'File archived with timestamp: {archived_filename}')

# Example usage:
directory_to_archive = '/AppDev/CEDL/etl/SrcFiles/lg/visit'
file_pattern_to_match  = 'output*.csv'

archive_files_with_timestamp(directory_to_archive, file_pattern_to_match)

###################################################################################




