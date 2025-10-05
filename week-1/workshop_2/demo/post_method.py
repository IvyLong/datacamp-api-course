import requests
import json

# 1. Define Request (URL and Method)
url = "https://jsonplaceholder.typicode.com/posts" # Endpoint for creating posts

# 2. Handle Headers: Necessary for POST to define data type and Auth (though fake here)
my_headers = {
    "Content-Type": "application/json",
    # Example of a Bearer Token (even if fake for this public API)
    "Authorization": "Bearer fake-token-12345" 
}

# 3. Serialize Data: The Python dictionary we want to send
my_thought_data = {
    "title": "My first thought submission",
    "body": "This is the data payload sent from the client.",
    "userId": 99 
}

print(f"\n--- Sending POST request to: {url} ---")
print(f"Sending JSON data: {my_thought_data}")

# 4. Send Request: The 'json' argument automatically serializes my_thought_data
response = requests.post(
    url, 
    headers=my_headers, 
    json=my_thought_data # The key difference from the 'data' argument
)

# 7. Check Status
if response.status_code == 201: # 201 Created is the standard for a successful POST
    print("\nSTATUS: 201 CREATED (Success) 🎉")
    
    # 6. Deserialize Data
    new_post = response.json()
    
    # The server confirms the creation and assigns a new ID
    print(f"Server-Assigned ID: {new_post['id']}")
    print(f"Confirmed Title: {new_post['title']}")
    
else:
    print(f"ERROR: Received status code {response.status_code}")