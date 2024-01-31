import requests
import json
import boto3

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

def read_json_from_s3(bucket_name, key):
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        return json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        print(f"Error reading JSON from S3: {e}")
        return None

def send_json_to_api(api_url, access_token, json_data):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.post(api_url, headers=headers, json=json_data)
    return response

# API credentials
api_url = "https://myevolvvnshealthdev.netsmartcloud.com/api/session/authenticate"
loginname = "apiuser3"
password = "abc123"

# Get the access token or text_response
access_token = get_access_token(api_url, loginname, password)

print(f"Access Token = > {access_token}")

# Read JSON from S3
bucket_name = "vnsny-das-landing-test"
json_key = "OUTGOING/MYEVOLV/ENCOUNTER_ALERTS/hospitalization.json"
json_data = read_json_from_s3(bucket_name, json_key)

if json_data:
    # Send JSON to API
    api_response = send_json_to_api(api_url, access_token, json_data)
    print(f"API Response: {api_response.text}")
else:
    print("Failed to read JSON from S3.")
