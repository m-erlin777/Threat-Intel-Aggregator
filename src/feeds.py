import requests
import logging

def fetch_feed(url, name):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        logging.info(f"Fetched {len(resp.text.splitlines())} lines from {name}")
        return resp.text
    except Exception as e:
        logging.error(f"Error fetching {name}: {e}")
        return ""

def fetch_all_feeds(feeds):
    results = {}
    for feed in feeds:
        raw = fetch_feed(feed["url"], feed["name"])
        results[feed["name"]] = {"raw": raw, "format": feed.get("format", "text")}
    return results
