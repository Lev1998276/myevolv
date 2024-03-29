import requests
import json

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
            # Handle text/plain response (adjust this part based on your needs)
            text_response = response.text
            #print(f"Received text/plain response: {text_response}")
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

api_url = "https://myevolvvnshealthdev.netsmartcloud.com/api/session/authenticate"
loginname = "apiuser3"
password = "abc123"

# Get the access token or text_response
access_token = get_access_token(api_url, loginname, password)

print(f"Access Token = > {access_token}")


