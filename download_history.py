import os
import json
import shutil
import sqlite3
from datetime import datetime, timedelta
from ops import db_location

def insert_download_history(browser_name, url, referrer, target_path, filename, start_time, end_time, received_bytes, total_bytes, mime_type):
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()

    # Assuming the download_history table schema has been updated to include referrer and target_path columns
    cursor.execute("""
        INSERT INTO download_history (browser_name, url, referrer, target_path, filename, start_time, end_time, received_bytes, total_bytes, mime_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (browser_name, url, referrer, target_path, filename, start_time, end_time, received_bytes, total_bytes, mime_type))

    connection.commit()
    connection.close()

class BrowserHistory:
    def __init__(self, browser_name="Chrome"):
        if browser_name == "Chrome":
            self._user_data = os.getenv("LOCALAPPDATA") + "\\Google\\Chrome\\User Data"
        elif browser_name == "Brave":
            self._user_data = os.getenv("LOCALAPPDATA") + "\\BraveSoftware\\Brave-Browser\\User Data"
        elif browser_name == "Edge":
            self._user_data = os.getenv("LOCALAPPDATA") + "\\Microsoft\\Edge\\User Data"
        else:
            raise ValueError("Unsupported browser.")
        self.browser_name = browser_name
        
    def _convert_time(self, chrome_time):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)

    def convert_size(self, size_bytes):
        suffixes = ['B', 'KB', 'MB', 'GB']
        suffix_index = 0
        size = float(size_bytes)
        while size >= 1024 and suffix_index < len(suffixes) - 1:
            size /= 1024
            suffix_index += 1
        return f"{size:.2f} {suffixes[suffix_index]}"

    def get_file_path(self, filename):
        for root, dirs, files in os.walk(self._user_data):
            if filename in files:
                return os.path.join(root, filename)
        return None

    def get_browser_downloads(self):
        history_db_path = self.get_file_path("History")
        if history_db_path:
            history_db_copy = os.getenv("TEMP") + f"\\{self.browser_name}_History.db"
            shutil.copy2(history_db_path, history_db_copy)
            conn = sqlite3.connect(history_db_copy)
            c = conn.cursor()
            c.execute("SELECT tab_url, referrer, target_path, start_time, end_time, received_bytes, total_bytes, last_access_time, mime_type FROM downloads order by end_time desc")
            for row in c.fetchall():
                # Extract filename from target_path
                filename = os.path.basename(row[2])
                # Convert times to readable format
                start_time = self._convert_time(row[3])
                end_time = self._convert_time(row[4])
                # Insert into database with referrer and target_path
                insert_download_history(self.browser_name, row[0], row[1], row[2], filename, start_time, end_time, row[5], row[6], row[8])
            c.close()
            conn.close()
            os.remove(history_db_copy)

if __name__ == "__main__":
    for browser in ["Chrome", "Brave", "Edge"]:
        bh = BrowserHistory(browser)
        bh.get_browser_downloads()
    print("Collecting Download History....")
