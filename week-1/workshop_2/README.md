# Workshop 2: Thought Tagger - API Integration with Python

## 🎯 Workshop Overview

Welcome to Workshop 2 of our API course! This is a **hands-on implementation workshop** where you'll learn API integration by completing skeleton code with TODO comments.

### 🎓 Workshop Format

**This is NOT a copy-paste tutorial!** You will:
1. **Read** the provided skeleton code with TODO comments
2. **Implement** the missing API integration parts yourself
3. **Test** your implementation against working reference solutions
4. **Learn** by doing, debugging, and comparing approaches

### What You'll Build

A "Thought Tagger" command-line application that:
- Takes a "thought of the day" as input
- Sends it to Google's Gemini AI API using raw HTTP requests
- Returns relevant tags that capture the thought's essence
- Uses the Python `requests` library for HTTP communication

### Learning Objectives

By the end of this workshop, you will:
- **Implement** API calls using raw HTTP requests with the `requests` library
- **Understand** how to construct API endpoints, headers, and payloads
- **Practice** handling API authentication and error management
- **Work** with Docker containers for consistent development environments
- **Compare** raw HTTP vs SDK approaches by seeing both solutions

## 🏗️ Project Structure

```
workshop_2/
├── README.md                           # This file
├── Dockerfile                          # Container configuration
├── requirements.txt                    # Python dependencies
├── auto/
│   └── run                            # Automated execution script
├── exercise/
│   └── raw_http/
│       └── thought_tagger.py          # Your implementation (complete the TODOs)
└── solutions/                          # Complete solutions (for comparison)
    ├── raw_http/
    │   └── thought_tagger.py          # Working raw HTTP implementation
    └── sdk/
        └── thought_tagger.py          # Working SDK implementation
```

## 🚀 Quick Start

### Prerequisites

1. **Docker**: Ensure Docker is installed and running on your system
2. **Gemini API Key**: Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Setup

1. **Set your API key** (required for both solutions):
   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   ```

2. **Navigate to the workshop directory**:
   ```bash
   cd workshop_2
   ```

3. **Test the complete solutions** (to see expected behavior):
   ```bash
   # Test raw HTTP solution
   ./auto/run "Today I learned that small steps lead to big changes" --solution-raw
   
   # Test SDK solution  
   ./auto/run "The best time to plant a tree was 20 years ago" --solution-sdk
   
   # Compare both solutions side by side
   ./auto/run "Learning is a lifelong journey" --solutions
   ```

4. **Work on your implementation** (exercise version with TODOs):
   ```bash
   # Try your raw HTTP implementation (will fail until you complete TODOs)
   ./auto/run "Today I learned that small steps lead to big changes"
   ```

## 📚 Understanding API Integration Approaches

You'll implement the **Raw HTTP approach** and then compare it with the **SDK approach**:

### 1. Raw HTTP Implementation (Your Exercise)

**What you'll implement:**
- Uses the `requests` library for HTTP communication
- Manually constructs API endpoints and headers
- Handles JSON serialization/deserialization explicitly
- Provides full control over the HTTP request/response cycle

**Why learn this:**
- Understand HTTP fundamentals and API mechanics
- Works with any API (even without official SDKs)
- Essential for debugging network-level issues
- Foundation knowledge for all API integrations

### 2. SDK Implementation (Solution Comparison)

**What you'll see:**
- Uses Google's official `google-generativeai` library
- Abstracts away HTTP details
- Provides type safety and better error handling
- Follows best practices established by the API provider

**When to use SDKs:**
- When official SDKs are available
- For production applications (better reliability)
- When you want to focus on business logic rather than API mechanics
- For faster development cycles

## 🔧 Technical Deep Dive

### API Integration Patterns

Both implementations follow these key patterns:

1. **Authentication**: Using API keys via headers or SDK configuration
2. **Request Construction**: Building proper payloads for the Gemini API
3. **Error Handling**: Managing network failures and API errors gracefully
4. **Response Parsing**: Extracting meaningful data from API responses


## 🛠️ Detailed Usage

### Command Syntax

```bash
./auto/run "your thought of the day" [options]
```

**Parameters:**
- `thought`: Your thought text (must be quoted if it contains spaces)
- `--solution-raw`: Run the raw HTTP solution
- `--solution-sdk`: Run the SDK solution  
- `--solutions`: Run both solutions side by side

### Examples

```bash
# Work on your implementation (raw HTTP with TODOs)
./auto/run "Clean code is not written by following a set of rules"

# Test individual solutions
./auto/run "Success is not final, failure is not fatal" --solution-raw
./auto/run "Every expert was once a beginner" --solution-sdk

# Compare both approaches side by side
./auto/run "Today I realized the importance of asking good questions" --solutions
```

### Expected Output

```
🤔 Analyzing thought: "Today I learned that small steps lead to big changes"
📡 Making raw HTTP request to Gemini API...

✨ Generated Tags:
  1. personal-growth
  2. learning
  3. incremental-progress
  4. motivation
  5. self-improvement

📊 Total tags generated: 5
🔧 Method: Raw HTTP requests
```

## 🔍 Code Analysis

### Raw HTTP Implementation Highlights

```python
# Manual HTTP request construction
url = f"{self.base_url}/gemini-pro:generateContent"
headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": self.api_key
}

# Explicit payload creation
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "temperature": 0.7,
        "topK": 40,
        "topP": 0.95,
        "maxOutputTokens": 100,
    }
}

# Manual response handling
response = requests.post(url, headers=headers, json=payload, timeout=30)
```

### SDK Implementation Highlights

```python
# SDK configuration
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Simplified API call
response = model.generate_content(
    prompt,
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        top_k=40,
        top_p=0.95,
        max_output_tokens=100,
    )
)
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```
   Error: GEMINI_API_KEY environment variable is required
   ```
   **Solution**: Set your API key: `export GEMINI_API_KEY='your-key'`

2. **Docker Not Running**
   ```
   Error: Docker is not running
   ```
   **Solution**: Start Docker Desktop or Docker daemon

3. **Permission Denied**
   ```
   Permission denied: ./auto/run
   ```
   **Solution**: Make script executable: `chmod +x auto/run`

4. **Network Issues**
   ```
   Error making HTTP request: Connection timeout
   ```
   **Solution**: Check internet connection and firewall settings

### Debug Mode

For detailed debugging, you can run the Python scripts directly:

```bash
# Build the Docker image first
docker build -t thought-tagger-workshop .

# Run with debug output
docker run --rm -e GEMINI_API_KEY="$GEMINI_API_KEY" \
    -v "$(pwd):/app" -w /app \
    thought-tagger-workshop \
    python -u solutions/raw_http/thought_tagger.py "debug test"
```

## 🎓 Implementation Exercise

### 🎯 Your Mission: Implement Raw HTTP API Integration

The workshop provides skeleton code with TODO comments. Your task is to implement the missing parts to make the API calls work using the Python `requests` library!

### 📋 Exercise: Raw HTTP Implementation

**File**: `exercise/raw_http/thought_tagger.py`

**Your Tasks:**
1. **TODO 1**: Set the Gemini API base URL
   - Hint: `"https://generativelanguage.googleapis.com/v1beta/models"`

2. **TODO 2**: Construct the complete API endpoint
   - Hint: Append `/gemini-pro:generateContent` to the base URL

3. **TODO 3**: Create proper HTTP headers
   - Need: `Content-Type: application/json` and `x-goog-api-key: [your-key]`

4. **TODO 4**: Build the request payload
   - Structure: `{"contents": [{"parts": [{"text": "..."}]}], "generationConfig": {...}}`

5. **TODO 5**: Make the HTTP POST request
   - Use: `requests.post()` with proper parameters

6. **TODO 6**: Handle the HTTP response
   - Use: `response.raise_for_status()` for error checking

7. **TODO 7**: Parse the JSON response
   - Use: `response.json()` to get structured data

8. **TODO 8**: Extract text from the nested response structure
   - Navigate: `response_data["candidates"][0]["content"]["parts"][0]["text"]`

**Testing Your Implementation:**
```bash
# This should work once you complete all TODOs
./auto/run "Learning APIs is fun and challenging"

# Compare with the working raw HTTP solution
./auto/run "Learning APIs is fun and challenging" --solution-raw

# See both approaches side by side
./auto/run "Learning APIs is fun and challenging" --solutions
```

### 🎯 Success Criteria

You've successfully completed the workshop when:

✅ Your raw HTTP implementation generates tags for any thought  
✅ You understand how to construct HTTP requests manually  
✅ You can explain the difference between raw HTTP and SDK approaches  
✅ You've compared both solutions and understand the trade-offs  

### 💡 Debugging Tips

**Common Issues & Solutions:**

1. **"Empty response" errors**:
   - Check your API key is valid
   - Verify the request payload structure

2. **"JSON decode" errors**:
   - Print the raw response text
   - Check if the API returned an error message
   - Verify your request headers

3. **"Permission denied"**:
   - Make sure the run script is executable: `chmod +x auto/run`

## 📖 Additional Resources

### API Documentation
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)

### HTTP and REST APIs
- [HTTP Methods and Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [REST API Best Practices](https://restfulapi.net/)

### Python Libraries
- [Requests Documentation](https://requests.readthedocs.io/)
- [JSON Handling in Python](https://docs.python.org/3/library/json.html)

### Docker
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)

## 🤝 Next Steps

After completing this workshop, you'll be ready to:
1. Integrate any REST API into your Python applications
2. Choose between raw HTTP and SDK approaches based on project needs
3. Handle authentication, error management, and response parsing
4. Containerize your API-dependent applications

Continue to Workshop 3 where we'll explore building your own APIs using Flask/FastAPI!

---

**Happy coding! 🚀**

*If you encounter any issues or have questions, don't hesitate to ask for help.*
