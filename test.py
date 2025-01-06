import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
base_id = os.getenv("AIRTABLE_BASE_ID")

# 3. Your table name exactly as it appears in Airtable (e.g. 'Metrics')
table_name = "Metrics"

# 4. Set up the Airtable API endpoint
url = f"https://api.airtable.com/v0/{base_id}/{table_name}"

# 5. Configure the request headers
headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",  # Add 'Bearer ' prefix
    "Content-Type": "application/json"
}

# 6. Prepare the data to send
data_to_send = {
    "records": [
        {
            "fields": {
                "boilerplate_removal": 3,
                "sentence_reconstruction": 3,
                "content_preservation": 3,
                "formatting_accuracy": 3,
                "absence_commentary": 3,
                "overall_quality_score": 100,
                "grade": "A"
            }
        }
    ]
}

# 7. Make the POST request to create a new record
response = requests.post(url, headers=headers, json=data_to_send)

# 8. Print out the response from Airtable (for debugging or confirmation)
print(response.status_code)
print(response.json())
