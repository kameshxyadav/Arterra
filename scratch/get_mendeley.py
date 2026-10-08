import httpx
import re

url = "https://data.mendeley.com/datasets/9k56pwtvz9/1"
r = httpx.get(url, follow_redirects=True)
print("Status:", r.status_code)
links = set(re.findall(r'href="([^"]+)"', r.text))
for l in sorted(links):
    if any(k in l for k in ['download', 'files', 'api', 'zip', 'xlsx']):
        print(l)

# Also search for JSON scripts inside the page that might contain file download URLs
json_matches = re.findall(r'https?://[^\s"<>\'\\]+files[^\s"<>\'\\]+', r.text)
for j in set(json_matches):
    print("Match:", j)
