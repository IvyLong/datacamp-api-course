#!/usr/bin/env python3
"""
Thought Tagger - SDK Implementation
A command-line tool that sends a "thought of the day" to Google's Gemini API
and receives relevant tags using the official Google Generative AI SDK.
"""

import os
import sys
from typing import List
import google.generativeai as genai


class GeminiSDKClient:
    """Client for interacting with Gemini API using the official SDK."""
    
    def __init__(self, api_key: str):
        """Initialize the client with API key."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_tags(self, thought: str) -> List[str]:
        """
        Generate tags for the given thought using Gemini API.
        
        Args:
            thought (str): The thought text to analyze
            
        Returns:
            List[str]: List of generated tags
        """
        # Create the prompt for tag generation
        prompt = f"""
        Analyze the following thought and generate 3-5 relevant tags that capture its essence, themes, and mood.
        Return only the tags as a comma-separated list, nothing else.
        
        Thought: "{thought}"
        
        Tags:
        """
        
        try:
            # Generate content using the SDK
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_k=40,
                    top_p=0.95,
                    max_output_tokens=100,
                )
            )
            
            # Extract and parse tags from the response
            if response.text:
                generated_text = response.text.strip()
                tags = [tag.strip() for tag in generated_text.split(",")]
                return [tag for tag in tags if tag]  # Remove empty tags
            
            return ["general", "thought"]  # Fallback tags
            
        except Exception as e:
            print(f"Error generating content with SDK: {e}", file=sys.stderr)
            return ["error", "sdk-failed"]


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
    print("🔧 Using Google Generative AI SDK...")
    
    client = GeminiSDKClient(api_key)
    tags = client.generate_tags(thought)
    
    # Display results
    print("\n✨ Generated Tags:")
    for i, tag in enumerate(tags, 1):
        print(f"  {i}. {tag}")
    
    print(f"\n📊 Total tags generated: {len(tags)}")
    print("🔧 Method: Official Google Generative AI SDK")


if __name__ == "__main__":
    main()
