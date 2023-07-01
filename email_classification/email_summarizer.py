import vercel_ai
from pathlib import Path
import json


client = vercel_ai.Client()

"""TEXT_FILE_PATH = Path("/home/varad/Work/email_classification/static/sample.txt")
with open(TEXT_FILE_PATH, 'r') as f:
    text = f.read()

print(f"Input text : \n {text}")

print()

query = f"Summarize in maximum 5 lines : \n {text}"

result = ""
for chunk in client.generate("openai:gpt-3.5-turbo", query):
  result += chunk

print("Output text : ")
print(result)"""

print(json.dumps(client.model_ids, indent=2))