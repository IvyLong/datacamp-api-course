# Flask Tutorial Cheat Sheet 📝

## 🚀 Running the Server

```bash
# Start server (from project root)
./auto/run python week-2/tutorial/step-1-hello-world.py

# Stop server
Ctrl + C
```

## 🌐 Port Numbers

| Method | Port | Example URL |
|--------|------|-------------|
| **Docker** (`./auto/run`) | **5001** | `http://localhost:5001/` |
| Direct Python | 5000 | `http://localhost:5001/` |

⚠️ **Remember: Docker uses port 5001!**

## 🧪 Testing Endpoints

### Using curl
```bash
# GET request
curl http://localhost:5001/api/hello

# GET with query parameter
curl "http://localhost:5001/api/v1/thoughts?tag=flask"

# POST request
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"text": "My thought", "tags": ["test"]}'

# PUT request
curl -X PUT http://localhost:5001/api/v1/thoughts/1 \
  -H "Content-Type: application/json" \
  -d '{"text": "Updated", "tags": ["new"]}'

# DELETE request
curl -X DELETE http://localhost:5001/api/v1/thoughts/1
```

### Using Python
```python
import requests

# GET
r = requests.get("http://localhost:5001/api/v1/thoughts")
print(r.json())

# POST
data = {"text": "My thought", "tags": ["python"]}
r = requests.post("http://localhost:5001/api/v1/thoughts", json=data)
print(r.json())

# PUT
data = {"text": "Updated", "tags": ["new"]}
r = requests.put("http://localhost:5001/api/v1/thoughts/1", json=data)

# DELETE
r = requests.delete("http://localhost:5001/api/v1/thoughts/1")
```

## 📚 Flask Basics

### Create a route
```python
@app.route("/api/hello")
def hello():
    return "Hello!"
```

### Return JSON
```python
from flask import jsonify

@app.route("/api/data")
def data():
    return jsonify({"message": "Hello"})
```

### Handle multiple methods
```python
@app.route("/api/thoughts", methods=["GET", "POST"])
def thoughts():
    if request.method == "GET":
        return jsonify(all_thoughts)
    elif request.method == "POST":
        # create new thought
        pass
```

### Path parameters
```python
@app.route("/api/thoughts/<int:id>")
def get_thought(id):
    return jsonify({"id": id})
```

### Query parameters
```python
from flask import request

@app.route("/api/search")
def search():
    tag = request.args.get("tag")  # ?tag=flask
    return jsonify({"tag": tag})
```

### Get JSON body
```python
from flask import request

@app.route("/api/create", methods=["POST"])
def create():
    data = request.get_json()
    text = data["text"]
    tags = data["tags"]
    return jsonify({"created": True})
```

## 📊 HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH, DELETE |
| 201 | Created | Successful POST (resource created) |
| 400 | Bad Request | Invalid input/validation error |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | Wrong HTTP method |
| 500 | Server Error | Unexpected server error |

### Return status code
```python
return jsonify({"message": "Created"}), 201
```

## 🔍 Common Patterns

### Error response
```python
def error(code, message):
    return jsonify({"error": True, "message": message}), code

# Usage
return error(404, "Not found")
```

### Find by ID
```python
def find_by_id(items, id):
    for item in items:
        if item["id"] == id:
            return item
    return None
```

### Validation
```python
def validate(data):
    if not data:
        return False, "Body required"
    if "text" not in data:
        return False, "Text required"
    if len(data["text"]) < 5:
        return False, "Text too short"
    return True, None

# Usage
valid, error = validate(data)
if not valid:
    return jsonify({"error": error}), 400
```

## 🐛 Debugging

### Print to console
```python
print(f"Received: {data}")  # Shows in terminal
```

### Enable debug mode
```python
app.run(debug=True)  # Auto-reload + better errors
```

### Check what you're receiving
```python
@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    print(f"Got: {data}")  # Debug
    print(f"Type: {type(data)}")  # Debug
    return jsonify(data)
```

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Use port **5001** with Docker |
| Module not found | Rebuild Docker image |
| Changes not showing | Restart server (Ctrl+C, then rerun) |
| 400 Bad Request | Check Content-Type header |
| Port in use | Stop other server: `docker ps` |

## 📁 File Structure

```
step-1-hello-world.py      → Basic routes
step-2-json-response.py    → JSON data
step-3-multiple-routes.py  → Multiple endpoints
step-4-url-parameters.py   → /thoughts/<id>
step-5-query-parameters.py → ?tag=flask
step-6-post-request.py     → POST data
step-7-validation.py       → Input validation
step-8-full-crud.py        → Complete CRUD
```

---

💡 **Tip:** Keep this cheat sheet open while coding!

