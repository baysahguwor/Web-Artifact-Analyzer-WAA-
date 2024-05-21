import os
import sqlite3
from datetime import datetime, timedelta
from ops import db_location

def save_to_database(history_entries, browser_name):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()

        # Insert browsing history entries into the table
        for entry in history_entries:
            browser_name, url, title, last_visit_time, visit_count = entry
            last_visit_time_str = last_visit_time.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
            cursor.execute("INSERT INTO browsing_history (browser_name, url, title, last_visit_time, visit_count) VALUES (?, ?, ?, ?, ?)",
                           (browser_name, url, title, last_visit_time_str, visit_count))

        # Commit changes and close the connection
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"{browser_name} is locked. Unable to access the browsing history database.")
        # Log the error if needed

def get_browser_history(browser_name, history_path, query):
    try:
        # Connect to the browser history database
        connection = sqlite3.connect(history_path)
        cursor = connection.cursor()

        # Execute the query and fetch results
        cursor.execute(query)
        results = cursor.fetchall()

        # Close the connection
        connection.close()

        # Display the browsing history
        formatted_results = []
        for result in results:
            url, title, last_visit_time_micro, visit_count = result
            last_visit_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time_micro)
            formatted_results.append((browser_name, url, title, last_visit_time, visit_count))

        # Return the results for saving to the new database
        return formatted_results
    except Exception as e:
        print(f"{browser_name} is locked. Unable to access the browsing history database.")
        # Log the error if needed
        return []

if __name__ == "__main__":
    # For Brave browser
    brave_default_profile_path = os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Default")
    brave_history_path = os.path.join(brave_default_profile_path, "History")
    brave_query = "SELECT url, title, last_visit_time, visit_count FROM urls ORDER BY last_visit_time DESC"
    brave_history_entries = get_browser_history("Brave", brave_history_path, brave_query)
    save_to_database(brave_history_entries, "Brave")

    # For Microsoft Edge browser
    edge_default_profile_path = os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default")
    edge_history_path = os.path.join(edge_default_profile_path, "History")
    edge_query = "SELECT url, title, last_visit_time, visit_count FROM urls ORDER BY last_visit_time DESC"
    edge_history_entries = get_browser_history("Edge", edge_history_path, edge_query)
    save_to_database(edge_history_entries, "Edge")

    # For Chrome browser
    chrome_default_profile_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default")
    chrome_history_path = os.path.join(chrome_default_profile_path, "History")
    chrome_query = "SELECT url, title, last_visit_time, visit_count FROM urls ORDER BY last_visit_time DESC"
    chrome_history_entries = get_browser_history("Chrome", chrome_history_path, chrome_query)
    save_to_database(chrome_history_entries, "Chrome")

print("Collecting Browsing history ...")
