#!/usr/bin/env python3
"""
Step 1 Solution: Hello World - Exercise Solutions

This file contains the solutions to the exercises from step-1-hello-world.py

EXERCISES COMPLETED:
1. ✅ Add a new route at "/api/status" that returns "Server is running!"
2. ✅ Add a route at "/about" that returns your name
3. ✅ Test all routes in your browser
4. ✅ Handle 404 for non-existent URLs (Flask handles this automatically)
"""

from flask import Flask

# Create a Flask application instance
app = Flask(__name__)


@app.route("/")
def hello_world():
    """Handle GET requests to the root URL (/)"""
    return "Hello, World! Welcome to Flask!"


@app.route("/api/hello")
def hello_api():
    """Handle GET requests to /api/hello"""
    return "Hello from the API!"


# ==========================================
# EXERCISE SOLUTIONS
# ==========================================

@app.route("/api/status")
def api_status():
    """
    EXERCISE 1 SOLUTION:
    Add a new route at "/api/status" that returns "Server is running!"
    """
    return "Server is running!"


@app.route("/about")
def about():
    """
    EXERCISE 2 SOLUTION:
    Add a route at "/about" that returns your name
    """
    return "Created by: API Course Student - Learning Flask and REST APIs!"


# Bonus: Additional useful routes
@app.route("/api/version")
def api_version():
    """Bonus route: API version information"""
    return "API Version 1.0.0"


@app.route("/health")
def health_check():
    """Bonus route: Simple health check"""
    return "OK"


if __name__ == "__main__":
    print("🚀 Starting Flask server with Exercise Solutions...")
    print("📖 Available routes:")
    print("   http://localhost:5001/                    - Welcome message")
    print("   http://localhost:5001/api/hello           - API greeting")
    print("   http://localhost:5001/api/status          - ✅ Exercise 1")
    print("   http://localhost:5001/about               - ✅ Exercise 2")
    print("   http://localhost:5001/api/version         - 🎁 Bonus route")
    print("   http://localhost:5001/health              - 🎁 Bonus route")
    print("")
    print("   Try a non-existent route for 404 error:")
    print("   http://localhost:5001/doesnotexist        - 🔍 Exercise 4")
    print("")
    print("Press CTRL+C to stop the server")
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5000)


# ==========================================
# 📝 EXERCISE ANSWERS:
# ==========================================

"""
EXERCISE 3: Run the server and test all routes in your browser
- All routes should return plain text responses
- Each route serves different content

EXERCISE 4: What happens if you visit a URL that doesn't exist?
- Flask automatically returns a 404 "Not Found" error
- The error page shows "404 Not Found" with basic HTML
- This is Flask's built-in error handling for undefined routes
"""