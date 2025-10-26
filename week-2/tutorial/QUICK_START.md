# Quick Start - Flask Tutorial

## ✅ Setup Complete!

Your Flask tutorial is ready with 8 progressive exercises.

## 🚀 For Students

### Run an exercise:
```bash
# From project root
./auto/run python week-2/tutorial/step-1-hello-world.py
```

Then open: **http://localhost:5001**

(Note: Port 5001, not 5001, when using Docker!)

### To stop the server:
Press `Ctrl+C`

## 📚 Progression Path

1. **step-1-hello-world.py** - Your first Flask app
2. **step-2-json-response.py** - Return JSON data  
3. **step-3-multiple-routes.py** - Multiple endpoints
4. **step-4-url-parameters.py** - Dynamic URLs with `/thoughts/1`
5. **step-5-query-parameters.py** - Filtering with `?tag=flask`
6. **step-6-post-request.py** - Create resources with POST
7. **step-7-validation.py** - Input validation and errors
8. **step-8-full-crud.py** - Complete CRUD API

## 🧪 Testing Endpoints

### Browser
Just visit the URL for GET requests:
```
http://localhost:5001/api/v1/thoughts
```

### curl
```bash
# GET request
curl http://localhost:5001/api/v1/thoughts

# POST request
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"text": "My first thought!", "tags": ["learning"]}'
```

### Python
```python
import requests

# GET
response = requests.get("http://localhost:5001/api/v1/thoughts")
print(response.json())

# POST
data = {"text": "Learning Flask!", "tags": ["flask", "python"]}
response = requests.post("http://localhost:5001/api/v1/thoughts", json=data)
print(response.json())
```

## 💡 Tips

- Read comments in each file carefully
- Complete exercises at the end of each file
- Test your code after each change
- Compare with the solution in `week-2/solution/app.py`

## 🆘 Help

- **Can't connect?** → Check server is running and use port 5001
- **Module not found?** → Rebuild Docker image after editing requirements.txt
- **Port in use?** → Stop other servers or change port in code

## 📖 Next Steps

After completing all steps:
1. Review `week-2/solution/app.py` (the complete solution)
2. Try building your own API from scratch
3. Add features like database persistence, authentication, etc.

---

**Happy coding! 🎉**

