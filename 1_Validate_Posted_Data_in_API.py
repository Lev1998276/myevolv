import json
from requests.exceptions import HTTPError

SubmitURL = "your_api_endpoint_here"
PostData = {"key1": "value1", "key2": "value2"}  # Replace with your actual data

try:
    response = Session.post(SubmitURL, data=PostData)
    response.raise_for_status()  # No exception will be raised if the response is successful

    # Additional validation based on the response content
    try:
        json_response = response.json()
        # You can now check the JSON content and perform validation as needed
        # Example: Assuming the API returns a JSON with a key "success" indicating success
        if "success" in json_response and json_response["success"]:
            print("Data posted successfully!")
        else:
            print("Data post was not successful. Additional validation failed.")
    except json.JSONDecodeError:
        print("Invalid JSON in response. Additional validation failed.")

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    # Handle specific HTTP errors or perform error handling as needed

except Exception as err:
    print(f"An unexpected error occurred: {err}")
    # Handle unexpected errors

else:
    # Success
    print("No errors occurred during data posting.")



###############################   VERSION 2 ###############################################

{
  "error": {
    "code": 422,
    "message": "Validation Error",
    "details": {
      "email": ["Invalid email format. Please provide a valid email address."]
    }
  }
}


import json
from requests.exceptions import HTTPError

SubmitURL = "your_api_endpoint_here"
PostData = {"username": "john_doe", "email": "invalid_email"}  # Invalid email format intentionally

try:
    response = Session.post(SubmitURL, json=PostData)
    response.raise_for_status()

    try:
        json_response = response.json()
        if "error" in json_response:
            error_message = json_response["error"]["details"]["email"][0]
            print(f"API Error: {error_message}")
        else:
            print("Data posted successfully!")

    except json.JSONDecodeError:
        print("Invalid JSON in response. Additional validation failed.")

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    # Handle specific HTTP errors or perform error handling as needed

except Exception as err:
    print(f"An unexpected error occurred: {err}")
    # Handle unexpected errors

else:
    # Success
    print("No errors occurred during data posting.")
