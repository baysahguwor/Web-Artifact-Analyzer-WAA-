import os
import sqlite3
from datetime import datetime, timedelta
from ops import db_location

def save_to_database(suspicious_entries, browser_name):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()

        # Insert suspicious entries into the table
        for entry in suspicious_entries:
            browser_name, url, title, last_visit_time, visit_count = entry
            last_visit_time_str = last_visit_time.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
            cursor.execute("INSERT INTO suspicious_history (browser_name, url, title, last_visit_time, visit_count) VALUES (?, ?, ?, ?, ?)",
                           (browser_name, url, title, last_visit_time_str, visit_count))

        # Commit changes and close the connection
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"{browser_name} is locked. Unable to access the browsing history database.")
        # Log the error if needed

def get_suspicious_browsing_history(browser_name, history_path, query):
    try:
        # Connect to the browser history database
        connection = sqlite3.connect(history_path)
        cursor = connection.cursor()

        # Execute the query and fetch results
        cursor.execute(query)
        results = cursor.fetchall()

        # Close the connection
        connection.close()

        # Check for suspicious browsing history entries
        suspicious_entries = []
        for result in results:
            url, title, last_visit_time_micro, visit_count = result
            last_visit_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time_micro)
            # Define your malicious activity criteria here
            malicious_keywords = ["phishing", "malware", "virus", "trojan", "ransomware", "spyware", "adware", "scam"]
            for keyword in malicious_keywords:
                if keyword in title.lower() or keyword in url.lower():
                    suspicious_entries.append((browser_name, url, title, last_visit_time, visit_count))
                    break

        return suspicious_entries
    except Exception as e:
        print(f"{browser_name} is locked. Unable to access the browsing history database.")
        # Log the error if needed
        return []

if __name__ == "__main__":
    # For Brave browser
    brave_default_profile_path = os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Default")
    brave_history_path = os.path.join(brave_default_profile_path, "History")
    brave_query = "SELECT url, title, last_visit_time, visit_count FROM urls ORDER BY last_visit_time DESC"
    brave_suspicious_entries = get_suspicious_browsing_history("Brave", brave_history_path, brave_query)
    save_to_database(brave_suspicious_entries, "Brave")

    # For Microsoft Edge browser
    edge_default_profile_path = os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default")
    edge_history_path = os.path.join(edge_default_profile_path, "History")
    edge_query = "SELECT url, title, last_visit_time, visit_count FROM urls ORDER BY last_visit_time DESC"
    edge_suspicious_entries = get_suspicious_browsing_history("Edge", edge_history_path, edge_query)
    save_to_database(edge_suspicious_entries, "Edge")

    # For Chrome browser
    chrome_default_profile_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default")
    chrome_history_path = os.path.join(chrome_default_profile_path, "History")
    chrome_query = "SELECT url, title, last_visit_time, visit_count FROM urls ORDER BY last_visit_time DESC"
    chrome_suspicious_entries = get_suspicious_browsing_history("Chrome", chrome_history_path, chrome_query)
    save_to_database(chrome_suspicious_entries, "Chrome")
