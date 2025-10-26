#!/usr/bin/env python3
"""
Step 1: Hello World - Your First Flask Application

Learning Objectives:
- Understand basic Flask app structure
- Create a simple route
- Run a Flask development server
- Return plain text responses

Concepts Introduced:
- Flask() app instance
- @app.route() decorator
- Running the development server
"""

from flask import Flask

# Create a Flask application instance
# __name__ helps Flask know where to look for resources
app = Flask(__name__)


# Define a route using the @app.route decorator
# This tells Flask what URL should trigger this function
@app.route("/")
def hello_world():
    """
    Handle GET requests to the root URL (/)
    Returns a simple text response
    """
    return "Hello, World! Welcome to Flask!"


@app.route("/api/hello")
def hello_api():
    """
    Handle GET requests to /api/hello
    Returns a greeting message
    """
    return "Hello from the API!"

# This block only runs when you execute this file directly
# It won't run if you import this file as a module
if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    print("📖 Try these URLs:")
    print("   http://localhost:5001/")
    print("   http://localhost:5001/api/hello")
    print("")
    print("Press CTRL+C to stop the server")
    print("")
    
    # Run the Flask development server
    # debug=True enables auto-reload and better error messages
    # host="0.0.0.0" makes the server accessible from other machines
    # port=5001 is the default Flask port
    app.run(debug=True, host="0.0.0.0", port=5001)


# ==========================================
# 🎯 EXERCISES:
# ==========================================
# 1. Add a new route at "/api/status" that returns "Server is running!"
# 2. Add a route at "/about" that returns your name
# 3. Run the server and test all routes in your browser
# 4. What happens if you visit a URL that doesn't exist?

