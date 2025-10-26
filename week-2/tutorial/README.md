# Week 2: Flask API Tutorial - Step by Step

This tutorial teaches you how to build a REST API with Flask through progressive exercises.

## 🎯 Learning Path

Each file builds on the previous one, introducing new concepts step by step:

1. **step-1-hello-world.py** - Your first Flask app
2. **step-2-json-response.py** - Returning JSON data
3. **step-3-multiple-routes.py** - Creating multiple endpoints
4. **step-4-url-parameters.py** - Using path parameters
5. **step-5-query-parameters.py** - Filtering with query strings
6. **step-6-post-request.py** - Accepting data with POST
7. **step-7-validation.py** - Input validation and error handling
8. **step-8-full-crud.py** - Complete CRUD API

## 🚀 How to Run Each Exercise

### Option A: Using Docker (Recommended)
```bash
# From the project root directory
./auto/run python week-2/tutorial/step-1-hello-world.py
```

The server will be available at: **`http://localhost:5001`** ⚠️

**Important:** Docker maps container port 5001 to host port **5001**, so you must use port **5001** in your URLs!

### Option B: Direct Python (requires Flask installed locally)
```bash
cd week-2/tutorial
python step-1-hello-world.py
```

The server will be available at: `http://localhost:5001`

## 📝 Testing Your API

### Using curl (with Docker - port 5001)
```bash
# GET request
curl http://localhost:5001/
curl http://localhost:5001/api/hello

# POST request
curl -X POST http://localhost:5001/api/thoughts \
  -H "Content-Type: application/json" \
  -d '{"text": "My first thought", "tags": ["learning"]}'
```

### Using Python requests (with Docker - port 5001)
```python
import requests

# GET request
response = requests.get("http://localhost:5001/api/hello")
print(response.json())

# POST request
data = {"text": "My first thought", "tags": ["learning"]}
response = requests.post("http://localhost:5001/api/thoughts", json=data)
print(response.json())
```

**Note:** If running directly with Python (not Docker), use port **5001** instead of **5001**.

### Using Browser
Simply open your browser and navigate to the URLs for GET requests.

## 💡 Tips

- Read the comments in each file carefully
- Try modifying the code to experiment
- Test each endpoint after implementing it
- Compare your code with the solution if you get stuck
- Use `Ctrl+C` to stop the server

## 🎓 Learning Objectives

By the end of this tutorial, you will understand:
- How Flask routes work
- The difference between GET and POST requests
- How to work with JSON in Flask
- Path and query parameters
- Request validation
- Error handling
- Building a complete REST API

---

**Ready to start?** Open `step-1-hello-world.py` and let's begin! 🚀

