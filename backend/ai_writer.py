import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat"
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek-ai/deepseek-coder"  # or "deepseek-chat"

def generate_blog(metadata):
    prompt = f"""
You're a technical blogger. Write a blog post based on the following GitHub repository:

Tech Stack: {', '.join(metadata.get('tech_stack', []))}

README:
{metadata.get('readme', '')[:1000]}

Code Snippets:
{''.join([f"{file['filename']}:\n{file['snippet']}\n" for file in metadata.get('files', [])[:3]])}

Write a well-structured blog in markdown format with the following sections:
- Introduction
- Features
- How it Works
- Sample Code
- Conclusion
"""

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"OpenRouter error {response.status_code}: {response.text}"

    except Exception as e:
        return f"OpenRouter request failed: {str(e)}"
