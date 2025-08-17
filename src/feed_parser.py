import pandas as pd
import logging
import io
import json
from stix2 import parse as stix_parse

class ThreatFeedParser:
    def __init__(self, feeds):
        """
        feeds: dict { 'feed_name': 'feed_url' }
        data: populated externally with raw content and format per feed
        """
        self.feeds = feeds
        self.data = {}
        self.parsed_data = pd.DataFrame()

    def parse_feed(self, name, raw_content, fmt="text"):
        """
        Parse raw feed content into a pandas DataFrame.
        Supports formats: text (line-by-line), csv, json, stix.
        """
        try:
            if fmt.lower() == "csv":
                df = pd.read_csv(io.StringIO(raw_content), comment='#', header=None, names=["indicator"])
            elif fmt.lower() == "json":
                parsed = json.loads(raw_content)
                df = pd.json_normalize(parsed)
            elif fmt.lower() == "stix":
                stix_obj = stix_parse(raw_content)
                indicators = [i for i in stix_obj if i.get("type") == "indicator"]
                df = pd.DataFrame(indicators)
            else:
                # Default: text/plain, one indicator per line
                lines = [line for line in raw_content.splitlines() if line.strip() and not line.startswith("#")]
                df = pd.DataFrame({"indicator": lines})
        except Exception as e:
            logging.error(f"[!] Error parsing feed {name} (format={fmt}): {e}")
            df = pd.DataFrame(columns=["indicator"])

        df["feed"] = name
        return df

    def to_dataframe(self):
        """
        Combine all parsed feeds into a single DataFrame.
        Each row: { feed: <feed name>, indicator: <IP/domain/etc.> }
        """
        all_rows = []
        for name, content_dict in self.data.items():
            raw = content_dict.get("raw", "")
            fmt = content_dict.get("format", "text")
            df = self.parse_feed(name, raw, fmt)
            all_rows.append(df)

        if all_rows:
            df = pd.concat(all_rows, ignore_index=True)
        else:
            df = pd.DataFrame(columns=["indicator", "feed"])

        logging.info(f"Parsed {len(df)} indicators from {len(self.data)} feeds")
        self.parsed_data = df
        return df
