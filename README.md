# Threat-Intel-Aggregator
A Python-based tool designed to automatically fetch, parse, normalize, and store threat intelligence indicators from multiple OSINT feeds in various formats, including CSV, JSON, STIX, and plain text. Stores all indicators in a SQLite database for analysis or integration with downstream tools.

## Features
- Fetches threat intelligence from multiple OSINT sources
- Supports CSV, JSON, STIX and plain text feed formats
- Logs all operations with configurable verbosity
- Stores parsed indicators in a SQLite database
- Command-line toggle for safe test-fetch operations without database writes
- Modular architecture for easy addition of new feeds or parsers

### Installation:
```
Placeholder
```

### Configuration:
- Edit config.yaml to add, remove or update OSINT feeds
- Specify logging level and database storage path
```
feeds:
  - name: Example
    url: "https://example.com/example.csv"
    format: "csv"
```

### Usage:
Test-fetch (No database writes):

`python main.py --test-fetch`

Full run (Parse and store):

`python main.py`

### Output:
- Database: `data/threatintel.db` with table `indicators` (columns: `id`, `feed`, `indicator`, `added_at`)
- Logs: `data/aggregator.log`
```
EXAMPLE:
[INFO] Threat Intel Aggregator started.
[INFO] Processed feeds: SSLBL Botnet C2 (format=csv) - 13 indicators
[INFO] Threat Intel Aggregator finished successfully.
```
