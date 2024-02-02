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

def read_json_from_s3(bucket_name, key):
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        return json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        print(f"Error reading JSON from S3: {e}")
        return None

def send_json_to_api(target_api_url, access_token, json_data):
    #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    headers = {
        'token': access_token,
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }
    print(headers)
    response = requests.post(target_api_url, headers=headers, json=json_data)
    return response

# API credentials
api_url = "https://myevolvvnshealthdev.netsmartcloud.com/api/session/authenticate"
loginname = "apiuser3"
password = "abc123"

# Get the access token or text_response
access_token_temp = get_access_token(api_url, loginname, password)
access_token = access_token_temp.strip()

print("\n")
print(f"Access Token = > {access_token}")
print("\n")

# Read JSON from S3
bucket_name = "vnsny-das-landing-test"
json_key = "OUTGOING/MYEVOLV/ENCOUNTER_ALERTS/hospitalization.json"
json_data = read_json_from_s3(bucket_name, json_key)


print(json.dumps(json_data, indent = 4))
print("\n")

target_api_url = "https://myevolvvnshealthdev.netsmartcloud.com/api/Forms/ImportSystem/FormImport"


#headers = {'Authorization': access_token,'Content-Type': 'text/plain'}
headers = {
        'token': access_token,
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }
print(headers)
response = requests.post(target_api_url, json=json_data, headers=headers)

print(response)


if response.status_code == 200:
    print("Token is valid. Access granted.")
else:
    print(f"Error: {response.status_code} - {response.text}")

#if json_data:
#     # Send JSON to API
#     api_response = send_json_to_api(target_api_url, access_token, json_data)
#     print(f"API Response status code: {api_response.status_code}")
#     print(f"API Response: {api_response.text}")
# else:
#     print("Failed to read JSON from S3.")


