import httpx
import json

# Mendeley Data public API v1 / v2 endpoints
urls = [
    "https://api.mendeley.com/datasets/9k56pwtvz9",
    "https://data.mendeley.com/api/datasets/9k56pwtvz9",
    "https://data.mendeley.com/public-files/datasets/9k56pwtvz9",
    "https://data.mendeley.com/public-api/datasets/9k56pwtvz9",
    "https://data.mendeley.com/public-files/datasets/9k56pwtvz9/1",
]

for url in urls:
    try:
        r = httpx.get(url, follow_redirects=True, headers={"Accept": "application/json"})
        print(url, r.status_code)
        if r.status_code == 200:
            print(r.text[:500])
    except Exception as e:
        print(url, e)
