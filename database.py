import sqlite3
from ops import db_location



def create_database():
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS browsing_history (
            browser_name TEXT,
            url TEXT,
            title TEXT,
            last_visit_time DATETIME,
            visit_count INTEGER
        )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS suspicious_history (
                browser_name TEXT,
                url TEXT,
                title TEXT,
                last_visit_time DATETIME,
                visit_count INTEGER
            )
        """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS download_history (
            browser_name TEXT,
            url TEXT,
            referrer TEXT, 
            target_path TEXT,
            filename TEXT,
            start_time DATETIME,
            end_time DATETIME,
            received_bytes INTEGER,
            total_bytes INTEGER, 
            mime_type TEXT
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cookies (
            browser_name TEXT,
            name TEXT,
            value TEXT,
            domain TEXT,
            path TEXT,
            expires_utc DATETIME,
            is_secure INTEGER,
            is_httponly TEXT
        )
    """)


    cursor.execute("""
            CREATE TABLE IF NOT EXISTS credentials (
                browser_name TEXT,
                url TEXT,
                username TEXT,
                password TEXT
            
            )
        """)


    cursor.execute("""
            CREATE TABLE IF NOT EXISTS examiner (
                ex_name TEXT,
                case_no TEXT,
                case_ref TEXT,
                desc TEXT,
                date_time DATETIME,
                phone TEXT,
                email TEXT,
                pc_infor TEXT
            )
        """)     


    connection.commit()
    connection.close()
create_database()
#db_location()