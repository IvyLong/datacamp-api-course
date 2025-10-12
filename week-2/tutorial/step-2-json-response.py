#!/usr/bin/env python3
"""
Step 2: JSON Responses - Returning Structured Data

Learning Objectives:
- Return JSON instead of plain text
- Use the jsonify() function
- Understand Content-Type headers
- Return different data structures

Concepts Introduced:
- jsonify() for JSON responses
- Python dictionaries → JSON objects
- Python lists → JSON arrays
- HTTP response status codes
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    """Return a simple text response (like Step 1)"""
    return "Welcome! Try /api/message for JSON data"


@app.route("/api/message")
def get_message():
    """
    Return a JSON object
    jsonify() converts a Python dict to JSON and sets Content-Type header
    """
    return jsonify({
        "message": "Hello, JSON!",
        "status": "success"
    })


@app.route("/api/user")
def get_user():
    """
    Return a more complex JSON object with nested data
    """
    user = {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "active": True,
        "roles": ["user", "admin"]
    }
    return jsonify(user)


@app.route("/api/thoughts")
def get_thoughts():
    """
    Return a JSON array (list of objects)
    This is common for listing resources
    """
    thoughts = [
        {
            "id": 1,
            "text": "Flask makes APIs easy!",
            "tags": ["flask", "python"]
        },
        {
            "id": 2,
            "text": "JSON is the language of APIs",
            "tags": ["json", "api-design"]
        },
        {
            "id": 3,
            "text": "Practice makes perfect",
            "tags": ["learning", "growth"]
        }
    ]
    return jsonify(thoughts)


@app.route("/api/stats")
def get_stats():
    """
    Return JSON with different data types
    """
    stats = {
        "total_thoughts": 42,
        "total_users": 15,
        "average_tags_per_thought": 2.3,
        "server_status": "healthy",
        "features": ["thoughts", "tags", "filtering"],
        "maintenance_mode": False
    }
    return jsonify(stats)


if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    print("📖 Try these endpoints:")
    print("   http://localhost:5001/api/message")
    print("   http://localhost:5001/api/user")
    print("   http://localhost:5001/api/thoughts")
    print("   http://localhost:5001/api/stats")
    print("")
    print("💡 Tip: Use browser DevTools (F12) to see the JSON response and headers")
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5000)


# ==========================================
# 🎯 EXERCISES:
# ==========================================
# 1. Create a route "/api/product" that returns a product with:
#    - id, name, price, in_stock, categories
#
# 2. Create a route "/api/products" that returns a list of 3 products
#
# 3. Test your endpoints using:
#    - Your browser
#    - curl: curl http://localhost:5001/api/products
#    - Python requests library
#
# 4. What is the Content-Type header of your JSON responses?
#    (Hint: Check in browser DevTools Network tab)

