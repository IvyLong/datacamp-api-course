import requests

# 1. Define Request (URL and implicit GET Method)
base_url = "https://jsonplaceholder.typicode.com"
endpoint = "/posts/1" # We are requesting the resource with ID 1

print(f"--- Sending GET request to: {base_url}{endpoint} ---")

# 4. Send Request
response = requests.get(base_url + endpoint)

# 7. Check Status
if response.status_code == 200:
    print("STATUS: 200 OK (Success) ✅")

    # 6. Deserialize Data (JSON Parsing)
    data = response.json()
    
    # Print a key piece of data
    print(f"Title of Post: {data['title']}")
    
else:
    print(f"ERROR: Received status code {response.status_code}")