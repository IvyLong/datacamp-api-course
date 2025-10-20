#!/usr/bin/env python3
"""
Step 2 Solution: JSON Responses - Exercise Solutions

This file contains the solutions to the exercises from step-2-json-response.py

EXERCISES COMPLETED:
1. ✅ Create a route "/api/product" that returns a product with required fields
2. ✅ Create a route "/api/products" that returns a list of 3 products
3. ✅ Test endpoints using browser, curl, and Python requests
4. ✅ Verify Content-Type header for JSON responses
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    """Return a simple text response"""
    return "Welcome! Try /api/message for JSON data"


@app.route("/api/message")
def get_message():
    """Return a JSON object"""
    return jsonify({
        "message": "Hello, JSON!",
        "status": "success"
    })


@app.route("/api/user")
def get_user():
    """Return a more complex JSON object with nested data"""
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
    """Return a JSON array (list of objects)"""
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
    """Return JSON with different data types"""
    stats = {
        "total_thoughts": 42,
        "total_users": 15,
        "average_tags_per_thought": 2.3,
        "server_status": "healthy",
        "features": ["thoughts", "tags", "filtering"],
        "maintenance_mode": False
    }
    return jsonify(stats)


# ==========================================
# EXERCISE SOLUTIONS
# ==========================================

@app.route("/api/product")
def get_product():
    """
    EXERCISE 1 SOLUTION:
    Create a route "/api/product" that returns a product with:
    - id, name, price, in_stock, categories
    """
    product = {
        "id": 101,
        "name": "Flask API Course",
        "price": 49.99,
        "in_stock": True,
        "categories": ["education", "programming", "web-development"],
        "description": "Learn to build REST APIs with Flask",
        "rating": 4.8,
        "reviews_count": 127
    }
    return jsonify(product)


@app.route("/api/products")
def get_products():
    """
    EXERCISE 2 SOLUTION:
    Create a route "/api/products" that returns a list of 3 products
    """
    products = [
        {
            "id": 101,
            "name": "Flask API Course",
            "price": 49.99,
            "in_stock": True,
            "categories": ["education", "programming", "web-development"]
        },
        {
            "id": 102,
            "name": "Python Data Science Kit",
            "price": 199.99,
            "in_stock": True,
            "categories": ["education", "data-science", "python"]
        },
        {
            "id": 103,
            "name": "REST API Design Book",
            "price": 29.99,
            "in_stock": False,
            "categories": ["education", "api-design", "reference"]
        }
    ]
    return jsonify(products)


# Bonus endpoints for additional practice
@app.route("/api/categories")
def get_categories():
    """Bonus: Return all available product categories"""
    categories = [
        {"name": "education", "count": 3},
        {"name": "programming", "count": 2},
        {"name": "web-development", "count": 1},
        {"name": "data-science", "count": 1},
        {"name": "python", "count": 2},
        {"name": "api-design", "count": 2},
        {"name": "reference", "count": 1}
    ]
    return jsonify({
        "total_categories": len(categories),
        "categories": categories
    })


@app.route("/api/inventory")
def get_inventory():
    """Bonus: Return inventory summary"""
    return jsonify({
        "total_products": 3,
        "in_stock": 2,
        "out_of_stock": 1,
        "total_value": 279.97,
        "last_updated": "2025-10-20T10:30:00Z"
    })


if __name__ == "__main__":
    print("🚀 Starting Flask server with Step 2 Exercise Solutions...")
    print("")
    print("📖 Original endpoints:")
    print("   http://localhost:5001/api/message")
    print("   http://localhost:5001/api/user")
    print("   http://localhost:5001/api/thoughts")
    print("   http://localhost:5001/api/stats")
    print("")
    print("📖 Exercise solution endpoints:")
    print("   http://localhost:5001/api/product          - ✅ Exercise 1")
    print("   http://localhost:5001/api/products         - ✅ Exercise 2")
    print("")
    print("📖 Bonus endpoints:")
    print("   http://localhost:5001/api/categories       - 🎁 Categories list")
    print("   http://localhost:5001/api/inventory        - 🎁 Inventory summary")
    print("")
    print("💡 Testing instructions:")
    print("")
    print("🌐 Browser: Open any endpoint URL")
    print("")
    print("📡 Curl examples:")
    print("   curl http://localhost:5001/api/product")
    print("   curl http://localhost:5001/api/products")
    print("   curl -i http://localhost:5001/api/products  # Shows headers")
    print("")
    print("🐍 Python requests example:")
    print("   import requests")
    print("   response = requests.get('http://localhost:5001/api/products')")
    print("   print(response.json())")
    print("   print(response.headers['Content-Type'])  # Should be 'application/json'")
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5000)


# ==========================================
# 📝 EXERCISE ANSWERS:
# ==========================================

"""
EXERCISE 3: Test endpoints using browser, curl, and Python requests
✅ Browser: Simply navigate to the URLs - JSON will be displayed
✅ Curl: Use the commands shown above
✅ Python: Use requests library as shown above

EXERCISE 4: What is the Content-Type header of your JSON responses?
✅ Answer: "application/json; charset=utf-8"
   
   This header tells the client:
   - The response body contains JSON data
   - The character encoding is UTF-8
   - Flask's jsonify() automatically sets this header
   
   You can verify this by:
   1. Browser DevTools → Network tab → Click on request → Check Response Headers
   2. Curl with -i flag: curl -i http://localhost:5001/api/products
   3. Python: print(response.headers['Content-Type'])
"""