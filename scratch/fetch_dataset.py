import httpx
import os

url = "https://data.mendeley.com/public-files/datasets/9k56pwtvz9/files/7c48113d-4edd-4eb1-bb7a-365c01a011da/file_downloaded"
out_path = os.path.join("data", "raw", "z_alizadeh_sani_extension.xlsx")

print(f"Downloading from {url} to {out_path}...")
r = httpx.get(url, follow_redirects=True)
print("Status code:", r.status_code, "Length:", len(r.content))

with open(out_path, "wb") as f:
    f.write(r.content)

print("Downloaded successfully!")
