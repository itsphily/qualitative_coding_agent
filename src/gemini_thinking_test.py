from google import genai

def main():
    # Replace 'GEMINI_API_KEY' with your actual API key
    client = genai.Client(api_key='GEMINI_API_KEY', http_options={'api_version': 'v1alpha'})
    
    # Example: Send a basic request using the Flash Thinking model
    response = client.models.generate_content(
        model='gemini-2.0-flash-thinking-exp',
        contents='Explain how RLHF works in simple terms.'
    )
    
    print(response.text)

if __name__ == '__main__':
    main()
