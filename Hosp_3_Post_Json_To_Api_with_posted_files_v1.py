import requests
import json
import boto3
import os
import time
import configparser



def read_config(file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config
    
    
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
    
 
 
def post_jsonfile_to_api(target_api_url, access_token, json_file):
    #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    headers = {
        'token': access_token,
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }
    #print(headers)
    response = requests.post(target_api_url, headers=headers, json=json_file)
    
    print(f"Response from API : {str(response.text)}")
    if response.status_code == 200:
       # Parse the JSON string
       response_dict = json.loads(str(response.text))
       # Extract the value of the "IsSuccess" key
       is_success = response_dict["IsSuccess"]
       print(f"Response from API is_success : {is_success}")
       return is_success
    else:
       # Parse the JSON string
       response_dict = json.loads(str(response.text))
       # Extract the value of the "IsSuccess" key
       is_success = response_dict["IsSuccess"]
       print(f"Response from API is_success : {is_success}")
       return is_success
    
    
def write_to_log(log_file, message):
    with open(log_file, 'a') as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")



if __name__ == "__main__":
    # Read the configuration
    config = read_config()
    
    
    # Access API values from the configuration
    api_auth_url = config.get('API', 'api_auth_url')
    api_target_url = config.get('API', 'api_target_url')
    api_loginname = config.get('API', 'api_loginname')
    api_password = config.get('API', 'api_password')
    
    # Access File/Paths  from the configuration
    json_file_path = config.get('Hospitalization', 'json_file_path') 
    
    
    print("\nConfig File Details \n")
    print(f'api_auth_url : {api_auth_url}')
    print(f'api_loginname : {api_loginname}')
    print(f'api_password : {api_password}')
    print(f'api_target_url : {api_target_url}')
    print(f'json_file_path : {json_file_path}')
    print("\n")
    
    
    
    # NOTE THIS WILL BE CREATED AT THE START OF THE PROGRAM
    os.system('touch posted_records.txt')
    posted_records_file = "posted_records.txt"
    
    posted_records = set()
    try:
        if os.path.exists(posted_records_file):
            with open(posted_records_file, "r") as file:
                lines = file.readlines()
                for each in lines:
                    posted_records.update(each)
        else:
            print(f"File {posted_records_file} doesn't exists") 
    except Exception as e:
        print(f"An error occurred: {e}")

       
    #Get the list of all json files that need to be posted
    json_files = [file for file in os.listdir(json_file_path) if file.endswith('.json')]
    
    for eachFile in json_files:
        print(f"\nFile {eachFile} is in progress to be posted")
        full_file_path = os.path.join(json_file_path, eachFile)
        if eachFile not in posted_records:
            with open(full_file_path, 'r') as file:
                json_data = json.load(file)
                access_token = get_access_token(api_auth_url,api_loginname,api_password)
                start_time = time.time()
                
                # Post the current file with the current access token
                success = post_jsonfile_to_api(api_target_url, access_token, json_data)
                elapsed_time = time.time() - start_time
                print(f"Success : {success}")
                
                
                elapsed_time = time.time() - start_time
                print(f"elapsed_time : {elapsed_time}")
                # Check if the file was transferred within 55 seconds
                if elapsed_time > 55:
                    print(f"Elapsed_time {elapsed_time} : Token expired or file not transferred within 60 seconds. Regenerating token\n")
                    time.sleep(30)
                    
                    # Regenerate token
                    access_token = get_access_token(api_auth_url,api_loginname,api_password)
                    print("Token regenerated...")
                    
                    # Attempt to repost the file
                    success = post_jsonfile_to_api(api_target_url, access_token, json_data)
                    
                    if not success:
                        print(f"File {eachFile} not transferred even after token regeneration.")
                        #write_to_log(log_file, f"Failed to transfer file: {eachFile}")
                    else:
                        posted_records.add(eachFile)
                        print(f"File {eachFile} not transferred even after token regeneration.\n")
                        #write_to_log(log_file, f"Successfully transferred file: {eachFile}")
                elif elapsed_time < 55 and success:
                    posted_records.add(eachFile)
                    print(f"File transferred within 60 seconds.")
                else:
                    print(f"File was not transferred and errored out with {success}")
        else:
             print("File as already processed")         
    
    
    for eachrecord in posted_records:
        print(f"{eachrecord} was successfully posted")
    
    
  
