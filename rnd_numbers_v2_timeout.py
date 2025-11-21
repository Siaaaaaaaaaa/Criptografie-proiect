import requests
import json
import time 

URL = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint16"

# The minimum wait time in seconds (The API limits requests to 1 per minute)
WAIT_TIME_SECONDS = 60

def fetch_quantum_number(api_url):
    """
    Makes a request to the QRNG API, handles HTTP and API errors,
    and returns the random number as an integer, or a special code 
    ('RATE_LIMIT_EXCEEDED'), or None upon failure.
    """
    try:
        # Make the HTTP request with a 10-second timeout
        print(f"Attempting to make a request to: {api_url}")
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success') == True:
                try:
                    # Successfully retrieve the first number from the 'data' array
                    random_int = data['data'][0]
                    return random_int
                except KeyError:
                    print(" API Consistency Error: 'success' was True, but the 'data' key was missing.")
                    return None
            else:
                error_message = data.get('message', 'Unknown API error message.')
                print(f"API Error (Success=False): {error_message}")
                return None
                
        elif response.status_code == 500 and "requests per minute" in response.text:
            return 'RATE_LIMIT_EXCEEDED' 
            
        else:
            print(f" HTTP Request Failed. Status Code: {response.status_code}")
            print(f"   Response: {response.text[:100]}...")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error during request: {e}")
        return None

quantum_number = None

while quantum_number is None or quantum_number == 'RATE_LIMIT_EXCEEDED':
    
    quantum_number = fetch_quantum_number(URL)
    if quantum_number is None:
        print("\nStopping. Could not obtain a number due to an unrecoverable error.")
        break
    
    elif quantum_number == 'RATE_LIMIT_EXCEEDED':
        print(f"\n Rate Limit Exceeded. Waiting for {WAIT_TIME_SECONDS} seconds before retrying...")
        time.sleep(WAIT_TIME_SECONDS + 5) 
        print("\n" + "="*50)
        print(f" Successfully Retrieved Quantum Random Integer: {quantum_number}")
        print("="*50)