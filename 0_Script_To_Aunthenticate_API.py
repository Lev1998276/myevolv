 Submit a POST request to https://myevolv.netsmartcloud.com/api/session/authenticate with the following in the body, in 
JSON format.  
1. Example: {"login_name":"your_login ", "password":"your_password"} 
i. login_name: staff username 
ii. password: staff’s password. This can be clear text or a SHA256 string. Sample C# to do SHA256: 



import requests
import json
import hashlib

def authenticate(login_name, password):
    # URL for authentication
    url = "https://example/api/session/authenticate"

    # Convert the password to SHA256 hash
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Prepare JSON data for the POST request
    data = {
        "login_name": login_name,
        "password": hashed_password  # You can use clear text if needed
    }

    # Convert data to JSON format
    json_data = json.dumps(data)

    # Set headers for the POST request
    headers = {
        "Content-Type": "application/json"
    }

    # Make the POST request
    response = requests.post(url, data=json_data, headers=headers)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        print("Authentication successful!")
        # You can do something with the response if needed
        # For example, print the response content
        print(response.text)
    else:
        print(f"Authentication failed with status code: {response.status_code}")
        # Print the response content for debugging purposes
        print(response.text)

# Example usage
login_name = "your_login"
password = "your_password"  # Replace with the actual password or its SHA256 hash
authenticate(login_name, password)
