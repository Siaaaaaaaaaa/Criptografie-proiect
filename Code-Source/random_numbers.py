# 1st method of generating random numers

import requests
url = "https://www.random.org/integers/?num=1&min=0&max=100&col=5&base=10&format=plain&rnd=new"

number = requests.get(url)

# checking if the request was successful 
if number.status_code == 200: 
    number_text = number.text.strip()

    try:
        rnd = int(number_text)
        print(rnd) 
    except ValueError as e: 
        print(f"Error converting to integer: {e}. Received text was: '{number_text}'")

else: 
    print(f"Request failed with status code: {number.status_code}") # Should NOT run if status is 200
    print("Response content (potential error message):")
    print(number.text[:200] + "...")