import sqlite3
import os
import glob
import platform
from datetime import datetime
from ops import db_location

""" def create_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Assuming the table creation code from your initial script is here

    connection.commit()
    connection.close() """


def find_firefox_file(filename):
    paths = {
        'Windows': os.path.join(os.getenv('APPDATA', ''), 'Mozilla', 'Firefox', 'Profiles'),
        'Darwin': os.path.join(os.getenv('HOME', ''), 'Library', 'Application Support', 'Firefox', 'Profiles'),
        'Linux': os.path.join(os.getenv('HOME', ''), '.mozilla', 'firefox')
    }
    os_name = platform.system()
    if os_name in paths:
        profile_path = paths[os_name]
        search_path = os.path.join(profile_path, '*', filename)
        files = glob.glob(search_path)
        if files:
            return files[0]
    return None

def insert_data_into_database(table_name, data):
    app_conn = sqlite3.connect(db_location)
    app_cur = app_conn.cursor()

    if table_name == "browsing_history":
        insert_query = """
        INSERT INTO browsing_history (browser_name, url, title, last_visit_time, visit_count) VALUES (?, ?, ?, ?, ?)
        """
    elif table_name == "cookies":
        insert_query = """
        INSERT INTO cookies (browser_name, name, value, domain, path, expires_utc, is_secure, is_httponly) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
    # Additional elif blocks for other tables if needed

    app_cur.executemany(insert_query, data)
    app_conn.commit()
    app_cur.close()
    app_conn.close()

def fetch_firefox_history():
    db_path = find_firefox_file('places.sqlite')
    if not db_path:
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = """
    SELECT moz_places.url, moz_places.title, moz_places.visit_count, moz_places.last_visit_date
    FROM moz_places
    ORDER BY moz_places.last_visit_date DESC
    """
    cur.execute(query)
    history_data = []
    for url, title, visit_count, last_visit_date in cur.fetchall():
        last_visit_date_formatted = datetime.utcfromtimestamp(last_visit_date / 1000000).strftime('%Y-%m-%d %H:%M:%S') if last_visit_date else None
        history_data.append(('Firefox', url, title, last_visit_date_formatted, visit_count))
    cur.close()
    conn.close()
    insert_data_into_database("browsing_history", history_data)

def fetch_firefox_cookies():
    db_path = find_firefox_file('cookies.sqlite')
    if not db_path:
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Adjust the SELECT statement based on your schema investigation
    query = """
    SELECT host, name, value, host, path, expiry, isSecure, isHttpOnly FROM moz_cookies
    """
    cur.execute(query)
    cookies_data = []
    for host, name, value, host, path, expiry, isSecure, isHttpOnly in cur.fetchall():
        expires_utc = datetime.utcfromtimestamp(expiry).strftime('%Y-%m-%d %H:%M:%S') if expiry else None
        cookies_data.append(('Firefox', name, value, host, path, expires_utc, isSecure, isHttpOnly))
    cur.close()
    conn.close()
    insert_data_into_database("cookies", cookies_data)

def fetch_firefox_downloads():
    # Placeholder function; adapt as necessary based on actual Firefox schema and your requirements
    pass

# Create database and tables
#create_database()

# Fetch and insert data into database
fetch_firefox_history()
fetch_firefox_cookies()
fetch_firefox_downloads()