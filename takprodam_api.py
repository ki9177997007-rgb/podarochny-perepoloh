"""Takprodam Publisher API client. Credentials are read only from environment."""
import json
import os
import sys
import urllib.error
import urllib.request

BASE = "https://api.takprodam.ru/v2/publisher/"

def get_sources():
    token = os.environ.get("TAKPRODAM_API_TOKEN")
    if not token:
        raise RuntimeError("Set TAKPRODAM_API_TOKEN as a GitHub Actions secret or environment variable")
    req = urllib.request.Request(
        BASE + "source/",
        headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

def main():
    data = get_sources()
    for source in data.get("items", []):
        print(json.dumps({
            "id": source.get("id"),
            "title": source.get("title"),
            "status": source.get("status"),
            "url": source.get("source_url"),
        }, ensure_ascii=False))
    # Do not publish affiliate links for unapproved sources.

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, urllib.error.URLError) as exc:
        print(f"Takprodam API check failed: {exc}", file=sys.stderr)
        sys.exit(1)
