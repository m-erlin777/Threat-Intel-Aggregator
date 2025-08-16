import argparse
import logging
import yaml
from pathlib import Path
from src.feeds import fetch_all_feeds
from src.feed_parser import ThreatFeedParser
from src.database import ThreatIntelDB

# Load config
CONFIG_PATH = Path(__file__).parent / "config.yaml"
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Command-line argument parser (TESTING)
parser = argparse.ArgumentParser(description="Threat Intel Aggregator")
parser.add_argument("--test-fetch", action="store_true",
                    help="Only fetch feeds and display line counts, then exit")
args = parser.parse_args()

# Fetch feeds once
feeds_list = config["feeds"]
feed_data = fetch_all_feeds(feeds_list)

if args.test_fetch:
    # SAFE TEST: Print feed info and exit
    for feed in feeds_list:
        name = feed["name"]
        fmt = feed.get("format", "text")
        lines = feed_data.get(name, {}).get("raw", "").splitlines()
        print(f"[TEST] {name} (format={fmt}): {len(lines)} lines fetched")
    exit(0)  # Skip logging, parsing, database storage

# Setup logging
log_path = Path(config["logging"]["file"])
log_path.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_path,
    level=getattr(logging, config["logging"]["level"].upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logging.info("Threat Intel Aggregator started.")

# Parse feeds with multi-format support
parser_obj = ThreatFeedParser({feed["name"]: feed["url"] for feed in feeds_list})
parser_obj.data = feed_data
df = parser_obj.to_dataframe()

# Log indicators per feed and format
for feed in feeds_list:
    name = feed["name"]
    fmt = feed.get("format", "text")
    indicators_count = len(df[df['feed'] == name])
    logging.info(f"Processed feed: {name} (format={fmt}) - {indicators_count} indicators")

logging.info(f"Parsed {len(df)} total indicators from {len(feeds_list)} feeds.")

# Store in database
db_path = config["database"]["path"]
db = ThreatIntelDB(db_path)
db.insert_dataframe(df)
db.close()

logging.info("Threat Intel Aggregator finished successfully.")
print(f"[+] Completed: {len(df)} indicators stored in {db_path}")
