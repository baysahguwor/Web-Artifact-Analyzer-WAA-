import os
from pathlib import Path
import shutil 


#create a global variable for database name and location
global db_location
db_location = "Evidence/database.db"

""" def dele():
    file_path = Path('database.db')
    file_path.unlink()
 """
def dele():
    if os.path.exists(db_location):
        os.remove(db_location)
    else:
        print("The file does not exist")


def create_evidence_folder():
    """Creates a folder named 'Evidence' in the current directory if it doesn't exist."""
    folder_path = 'Evidence'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

def delete_evidence_folder():
    """Deletes the folder named 'Evidence' in the current directory if it exists."""
    folder_path = 'Evidence'
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist or is not a directory.")

# Example usage
#create_evidence_folder()  # Call this function to create the folder
#delete_evidence_folder()  # Call this function to delete the folder
