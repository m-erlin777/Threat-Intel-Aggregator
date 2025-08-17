import sqlite3
import logging
from pathlib import Path
import pandas as pd

class ThreatIntelDB:
    def __init__(self, db_path: str):
        """
        Initialize database connection. Creates DB if it does not exist.
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure folder exists
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        """
        Creates main table for threat indicators if one doesn't exist.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feed TEXT NOT NULL,
            indicator TEXT NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.conn.execute(create_table_sql)
        self.conn.commit()
        logging.info("Threat indicators table ready.")

    def insert_dataframe(self, df: pd.DataFrame):
        """
        Insert pandas DataFrame into indicators table.
        Expects columns: ['feed', 'indicator']
        """
        if df.empty:
            logging.warning("DataFrame is empty. No data inserted.")
            return
        try:
            df.to_sql("indicators", self.conn, if_exists="append", index=False)
            logging.info(f"Inserted {len(df)} indicators into the database.")
        except Exception as e:
            logging.error(f"Failed to insert DataFrame: {e}")

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()
        logging.info("Database connection closed.")
