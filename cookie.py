import os
import sqlite3
from datetime import datetime, timedelta
import shutil  # Add this import statement
from ops import db_location

def insert_cookie(browser_name, name, value, domain, path, expires_utc, is_secure, is_httponly):
    try:
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()

        # Assuming the cookies table schema includes the following columns:
        # browser_name, name, value, domain, path, expires_utc, is_secure, is_httponly
        cursor.execute("""
            INSERT INTO cookies (browser_name, name, value, domain, path, expires_utc, is_secure, is_httponly)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (browser_name, name, value, domain, path, expires_utc, is_secure, is_httponly))

        connection.commit()
        connection.close()
    except Exception as e:
        print(f"{browser_name} is locked. Unable to access the cookies database.")
        # Log the error if needed

class BrowserCookie:
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

    def _convert_chrome_time_to_datetime(self, chrome_time):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)

    def get_file_path(self, filename):
        for root, dirs, files in os.walk(self._user_data):
            if filename in files:
                return os.path.join(root, filename)
        return None

    def get_browser_cookies(self):
        cookies_db_path = self.get_file_path("Cookies")
        if cookies_db_path:
            cookies_db_copy = os.getenv("TEMP") + f"\\{self.browser_name}_Cookies.db"
            try:
                shutil.copy2(cookies_db_path, cookies_db_copy)
                conn = sqlite3.connect(cookies_db_copy)
                c = conn.cursor()
                c.execute("SELECT name, value, host_key as domain, path, expires_utc, is_secure, is_httponly FROM cookies")
                for row in c.fetchall():
                    name, value, domain, path, expires_utc, is_secure, is_httponly = row
                    expires_utc = self._convert_chrome_time_to_datetime(expires_utc)
                    insert_cookie(self.browser_name, name, value, domain, path, expires_utc, is_secure, is_httponly)
                c.close()
                conn.close()
                os.remove(cookies_db_copy)
            except PermissionError:
                print(f"Permission denied accessing {self.browser_name} cookies database. Please make sure the browser is closed and try again.")
            except Exception as e:
                print(f"An error occurred while accessing {self.browser_name} cookies database: {str(e)}")
                # Log the error if needed
        else:
            print(f"Could not find {self.browser_name} cookies database.")

if __name__ == "__main__":
    for browser in ["Chrome", "Brave", "Edge"]:
        bc = BrowserCookie(browser)
        bc.get_browser_cookies()
    print("Collecting cookie data...")
