from google import genai
from dotenv import load_dotenv
import os

def main():
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
    
    # Example: Send a basic request using the Flash Thinking model
    response = client.models.generate_content(
        model='gemini-2.0-flash-thinking-exp',
        contents='Explain how RLHF works in simple terms.'
    )
    
    print(response.text)

if __name__ == '__main__':
    main()
