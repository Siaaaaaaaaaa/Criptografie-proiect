import requests
import json

url =("https://qrng.anu.edu.au/API/jsonI.php?length=1&type=unit16")

try:
    response = requests.get(url, timeout=10) # Added timeout for safety
    
    if response.status_code == 200:
        data = response.json()
        
        print("--- Full Response Data ---")
        print(json.dumps(data, indent=4))
        print("--------------------------")
        
        if data.get('success') == True:
            try:
                random_int = data['data'][0]
                print(f"\n Successfully Retrieved Random Integer: {random_int}")
            except KeyError:
                print("\n API Consistency Error: 'success' was True, but 'data' key was missing.")
                
        else:
            # FAILURE: Print the error message from the API
            error_message = data.get('message', 'Unknown API error message.')
            print(f"\n API Request Failed. Success was False.")
            print(f"   Error Message: {error_message}")
            
    else:
        # HTTP FAILURE: Handle non-200 status codes
        print(f"\n HTTP Request Failed. Status Code: {response.status_code}")
        print(f"   Response Text: {response.text[:100]}...") # Show beginning of response

except requests.exceptions.RequestException as e:
    print(f"\n Network Error during request: {e}")