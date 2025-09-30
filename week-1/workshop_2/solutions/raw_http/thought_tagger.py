#!/usr/bin/env python3
"""
Thought Tagger - Raw HTTP Implementation
A command-line tool that sends a "thought of the day" to Google's Gemini API
and receives relevant tags using raw HTTP requests.
"""

import json
import os
import sys
import requests
from typing import List, Dict, Any


class GeminiHTTPClient:
    """Client for interacting with Gemini API using raw HTTP requests."""
    
    def __init__(self, api_key: str):
        """Initialize the client with API key."""
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        
    def generate_tags(self, thought: str) -> List[str]:
        """
        Generate tags for the given thought using Gemini API.
        
        Args:
            thought (str): The thought text to analyze
            
        Returns:
            List[str]: List of generated tags
        """
        # Construct the API endpoint
        url = f"{self.base_url}/gemini-pro:generateContent"
        
        # Prepare the request headers
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        
        # Create the prompt for tag generation
        prompt = f"""
        Analyze the following thought and generate 3-5 relevant tags that capture its essence, themes, and mood.
        Return only the tags as a comma-separated list, nothing else.
        
        Thought: "{thought}"
        
        Tags:
        """
        
        # Prepare the request payload
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 100,
            }
        }
        
        try:
            # Make the HTTP request
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            # Parse the response
            response_data = response.json()
            
            # Extract the generated text
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                candidate = response_data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    generated_text = candidate["content"]["parts"][0]["text"].strip()
                    
                    # Parse tags from the response
                    tags = [tag.strip() for tag in generated_text.split(",")]
                    return [tag for tag in tags if tag]  # Remove empty tags
            
            return ["general", "thought"]  # Fallback tags
            
        except requests.exceptions.RequestException as e:
            print(f"Error making HTTP request: {e}", file=sys.stderr)
            return ["error", "request-failed"]
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}", file=sys.stderr)
            return ["error", "json-parse-failed"]
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return ["error", "unexpected"]


def main():
    """Main function to run the thought tagger."""
    # Check if thought is provided as command line argument
    if len(sys.argv) < 2:
        print("Usage: python thought_tagger.py \"Your thought of the day\"")
        print("Example: python thought_tagger.py \"Today I learned that small steps lead to big changes\"")
        sys.exit(1)
    
    # Get the thought from command line arguments
    thought = " ".join(sys.argv[1:])
    
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is required")
        print("Please set your Gemini API key: export GEMINI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Create the client and generate tags
    print(f"🤔 Analyzing thought: \"{thought}\"")
    print("📡 Making raw HTTP request to Gemini API...")
    
    client = GeminiHTTPClient(api_key)
    tags = client.generate_tags(thought)
    
    # Display results
    print("\n✨ Generated Tags:")
    for i, tag in enumerate(tags, 1):
        print(f"  {i}. {tag}")
    
    print(f"\n📊 Total tags generated: {len(tags)}")
    print("🔧 Method: Raw HTTP requests")


if __name__ == "__main__":
    main()
