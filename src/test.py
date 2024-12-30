from google import genai

# Replace the `project` and `location` values with appropriate values for
# your project.
client = genai.Client(
    vertexai=True, project='YOUR_CLOUD_PROJECT', location='us-central1'
)
response = client.models.generate_content(
    model='gemini-2.0-flash-exp', contents='How does AI work?'
)
print(response.text)