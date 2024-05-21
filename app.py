# app.py

import subprocess
from pc_infor import report

def main():
    # Call the function to create the database and its tables

    subprocess.run(["python", "database.py"])
    print("Evidence created successfully.")
    subprocess.run(["python", "browsing_history.py"])
    #print("Collecting Browsing History...")
    subprocess.run(["python", "download_history.py"])
    #print("Collecting Download History...")
    subprocess.run(["python", "credentials.py"])
   # print("Collecting Credentials ...")
    subprocess.run(["python", "suspecious.py"])
    #print("Collecting Possible Suspecious Data...")
    subprocess.run(["python", "cookie.py"])
    #print("Collecting Cookies Data...")
    subprocess.run(["python", "firefox.py"])
    print("Completing collection Data...")
    print("Installed browsers: ", report)
    print("All Done !!!")
    print("...........................................")
    print("You can now generate the report")
   


if __name__ == "__main__":
    main()
