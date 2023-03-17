import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://api.todoist.com/rest/v2/projects"
headers = {"Authorization": "Bearer " + os.getenv("TODOIST_TOKEN")}

response = requests.get(url, headers=headers)

print(response.json())
