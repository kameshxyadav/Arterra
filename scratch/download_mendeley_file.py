import httpx
import json

url = "https://data.mendeley.com/public-api/datasets/9k56pwtvz9"
r = httpx.get(url, headers={"Accept": "application/json"})
data = r.json()
print("Keys:", data.keys())
print("Files:", json.dumps(data.get("files", []), indent=2))
