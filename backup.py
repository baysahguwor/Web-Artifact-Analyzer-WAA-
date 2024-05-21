import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import sqlite3
from ops import delete_evidence_folder, create_evidence_folder, db_location
from pc_infor import report


# Ensure the database and table are setup correctly
""" def setup_database():
    connection = sqlite3.connect("database.db")  # Using the database name from your original script
    cursor = connection.cursor()
    # Assuming the table structure based on the INSERT statement provided in your old_script.py
 """
class CaseInformation:
    def __init__(self, parent):
        
        self.parent = parent
        self.parent.title("Case Information System")
        self.parent.state('zoomed')
        delete_evidence_folder() #delete previous database
        #setup_database()  # Ensure the database is setup before initializing the UI
        self.setup_layout()

    def display_installed_browsers(self):
        installed_browsers = ["Chrome", "Firefox", "Safari", "Edge", "Opera"]
        self.output_text.insert(tk.END, "Detected Installed Browsers:\n")
        for browser in installed_browsers:
            self.output_text.insert(tk.END, f"- {browser}\n")
        self.output_text.insert(tk.END, "\n")

    def setup_layout(self):
        self.left_frame = ttk.Frame(self.parent, padding="20 20 20 20")
        self.left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)

        self.right_frame = ttk.Frame(self.parent, padding="20 20 20 20")
        self.right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)

        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=2)
        self.parent.rowconfigure(0, weight=1)

        self.setup_case_entry_ui()
        self.setup_output_display_ui()

    def setup_case_entry_ui(self):
        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 11)

        # Adding additional fields for phone and email based on the original script
        fields = ["Case Name:", "Case Reference:", "Description:", "Date of Investigation:", "Examiner Name:", "Phone:", "Email:"]
        self.entries = {}
        for i, field in enumerate(fields):
            ttk.Label(self.left_frame, text=field, font=label_font).grid(row=i, column=0, sticky=tk.W, pady=5)
            if field == "Description:":
                entry = tk.Text(self.left_frame, height=5, width=50, font=entry_font)
            else:
                entry = ttk.Entry(self.left_frame, font=entry_font)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5)
            self.entries[field.strip(':')] = entry

        ttk.Button(self.left_frame, text="Save & Collect Evidence", command=self.save_case).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def setup_output_display_ui(self):
        ttk.Label(self.right_frame, text="Process Output:", font=("Helvetica", 14)).pack(anchor='nw', pady=5)
        self.output_text = tk.Text(self.right_frame, height=15, width=50, bg="white", fg="red", font=("Helvetica", 14))
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.right_frame, orient='vertical', command=self.output_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.output_text['yscrollcommand'] = scrollbar.set

    def execute_subprocess_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in process.stdout:
            if line:
                self.output_text.insert(tk.END, line)
                self.output_text.see(tk.END)
            self.parent.update_idletasks()
        process.stdout.close()
        process.wait()

    def save_case(self):
        self.output_text.delete('1.0', tk.END)
        self.display_installed_browsers() #Display installed browsers
        self.output_text.insert(tk.END, "\n\nSaving case and collecting evidence...\n")
        case_info = {
            "ex_name": self.entries["Examiner Name"].get(),
            "case_no": self.entries["Case Name"].get(),
            "case_ref": self.entries["Case Reference"].get(),
            "desc": self.entries["Description"].get("1.0", tk.END).strip(),
            "date_time": self.entries["Date of Investigation"].get(),
            "phone": self.entries["Phone"].get(),
            "email": self.entries["Email"].get(),
        }

        command = ["python", "app.py"]  # Placeholder command
        threading.Thread(target=self.execute_subprocess_command, args=(command,), daemon=True).start()
        self.save_case_to_database(case_info)

    def save_case_to_database(self, case_info):
        create_evidence_folder() #create the folder
        subprocess.run(["python", "database.py"])
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO examiner (ex_name, case_no, case_ref, desc, date_time, phone, email)
            VALUES (:ex_name, :case_no, :case_ref, :desc, :date_time, :phone, :email)
        ''', case_info)
        connection.commit()
        connection.close()
        self.output_text.insert(tk.END, "Case saved successfully.\n\nCollecting Evidence...\nPlease make sure all browsers are closed!\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaseInformation(root)
    root.mainloop()
