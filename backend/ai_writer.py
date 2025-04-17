import requests
import os
import json
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")
# Updated to use a valid model ID for OpenRouter
MODEL = "openai/gpt-3.5-turbo"  # Fallback to a commonly available model

def sanitize_text(text):
    """Sanitize text to ensure it can be safely processed and sent to API."""
    if not isinstance(text, str):
        return ""
    # Replace or remove problematic characters and ensure UTF-8 compatibility
    return text.encode('utf-8', errors='replace').decode('utf-8')

def generate_local_blog(metadata):
    """Generate a simple blog post locally when API is unavailable."""
    repo_name = metadata.get('repo_name', 'Unknown Repository')
    repo_url = metadata.get('repo_url', '')
    tech_stack = ', '.join(metadata.get('tech_stack', ['Unknown']))
    readme = metadata.get('readme', 'No README available.')[:500]  # Just use a short excerpt
    
    # Get first file snippet if available
    code_example = ""
    if metadata.get('files') and len(metadata.get('files')) > 0:
        first_file = metadata.get('files')[0]
        code_example = f"""
## Code Example

Here's a snippet from `{first_file.get('filename', 'example.py')}`:

```
{first_file.get('snippet', '# No code available')}
```
"""
    
    # Generate a simple blog structure
    blog = f"""# {repo_name}

## Introduction

This blog post explores the GitHub repository [{repo_name}]({repo_url}), which appears to be built using {tech_stack}.

## Overview

{readme}

## Features

Based on the repository analysis, here are the main features:

- Feature 1: The repository provides functionality related to {repo_name.replace('-', ' ')}
- Feature 2: It uses {tech_stack} to implement its core functionality
- Feature 3: It includes a well-structured codebase with multiple components

{code_example}

## Conclusion

The {repo_name} repository demonstrates a practical implementation of {tech_stack} technologies. It provides a solid foundation for understanding how these technologies can be used together effectively.
"""
    return blog

def generate_blog(metadata):
    """Generate a blog post based on repository metadata."""
    try:
        tech_stack = ', '.join(metadata.get('tech_stack', ['Unknown']))
        readme = sanitize_text(metadata.get('readme', ''))[:2000]
        repo_name = metadata.get('repo_name', 'Unknown Repository')
        repo_url = metadata.get('repo_url', '')
        
        # Build code snippet section
        code_snippets = ""
        for file in metadata.get('files', [])[:3]:
            filename = sanitize_text(file.get('filename', ''))
            snippet = sanitize_text(file.get('snippet', ''))
            code_snippets += f"### {filename}:\n```\n{snippet}\n```\n\n"

        # Create the prompt
        prompt = (
            f"Write a technical blog post about the GitHub repository '{repo_name}' ({repo_url}).\n\n"
            f"Tech Stack: {tech_stack}\n\n"
            f"README Excerpt:\n{readme}\n\n"
            f"Code Snippets:\n{code_snippets}\n\n"
            "Structure the blog post in markdown format with these sections:\n"
            "1. Introduction: Briefly explain what the repository is and its purpose\n"
            "2. Features: List and explain the key features or capabilities\n"
            "3. How it Works: Technical explanation of the architecture or approach\n"
            "4. Sample Code: Break down a simple example of how to use it\n"
            "5. Conclusion: Final thoughts and potential use cases\n\n"
            "Keep the tone professional but approachable. Include code examples where relevant."
        )

        # Debug the API key
        if not API_KEY:
            logger.error("OpenRouter API key not found. Please set OPENROUTER_API_KEY in your environment variables.")
            logger.info("Falling back to local blog generation")
            return generate_local_blog(metadata)
        
        key_preview = API_KEY[:4] + "..." + API_KEY[-4:] if len(API_KEY) > 8 else "***" 
        logger.info(f"Using API key starting with {key_preview}")
        
        # Try to use the API
        try:
            logger.info(f"Sending request to OpenRouter API for model: {MODEL}")
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1500
            }
            
            # Send the request
            response = requests.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            # Log the response status
            logger.info(f"OpenRouter API response status: {response.status_code}")
            
            # Check if the response is valid
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    logger.info("Successfully parsed JSON response")
                    
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        if "message" in response_data["choices"][0]:
                            content = response_data["choices"][0]["message"]["content"]
                            logger.info("Successfully extracted blog content")
                            return content
                        else:
                            logger.warning("Response format unexpected - missing 'message' field")
                    else:
                        logger.warning("Response format unexpected - missing 'choices' field")
                
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {str(e)}")
                    logger.info(f"Response content (first 200 chars): {response.text[:200]}")
            else:
                logger.error(f"API returned error code {response.status_code}")
                logger.info(f"Error response: {response.text[:200]}")
            
            # If we get here, something went wrong with the API
            logger.info("Falling back to local blog generation")
            return generate_local_blog(metadata)
            
        except Exception as e:
            logger.error(f"Exception during API request: {str(e)}")
            logger.info("Falling back to local blog generation")
            return generate_local_blog(metadata)
            
    except Exception as e:
        logger.error(f"Error in generate_blog function: {str(e)}")
        return generate_local_blog(metadata)