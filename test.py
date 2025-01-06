import requests
import json

# 1. Your API key or Personal Access Token
#    If using an API key, prefix with 'Bearer ' + api_key
#    If using a PAT, do the same.
AIRTABLE_API_KEY = "pat6Ip0yNXBnkTMtO.f0c610b8235924a52f259e3820b87bef6476fe13278eeb16357586b477088d6d"

# 2. Your base ID (from the API docs or base settings)
base_id = "appnPdkx0AZdemg7M"

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
