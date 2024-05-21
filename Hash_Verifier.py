import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import hashlib

class HashVerifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hash Verifier")

        # Style Configuration
        root.configure(bg='#334257')  # Background color
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10, 'bold'), borderwidth='4')
        style.configure('TLabel', background='#334257', foreground='#EEEEEE', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10), borderwidth='2')
        style.map('TButton', foreground=[('!active', '#EEEEEE'), ('active', '#FFD700')], background=[('!active','#476072'), ('active', '#FFA500')])

        # File path variable
        self.file_path = tk.StringVar()

        # Hash values variables
        self.hash_value1 = tk.StringVar()
        self.hash_value2 = tk.StringVar()

        # Create GUI elements organized in a grid
        self.import_button = ttk.Button(root, text="Import File", command=self.import_file)
        self.import_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.generate_button = ttk.Button(root, text="Generate Hash", command=self.generate_hash, state='disabled')
        self.generate_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.hash_value1_label = ttk.Label(root, text="Hash Value One:")
        self.hash_value1_label.grid(row=2, column=0, padx=10, sticky='w')

        self.hash_value1_entry = ttk.Entry(root, textvariable=self.hash_value1, state='readonly')
        self.hash_value1_entry.grid(row=3, column=0, padx=10, pady=5, sticky='ew')

        self.save_hash_button = ttk.Button(root, text="Save Hash", command=self.save_hash, state='disabled')
        self.save_hash_button.grid(row=4, column=0, padx=10, pady=10, sticky='ew')

        self.hash_value2_label = ttk.Label(root, text="Hash Value Two:")
        self.hash_value2_label.grid(row=0, column=1, padx=10, sticky='w')

        self.hash_value2_entry = ttk.Entry(root, textvariable=self.hash_value2)
        self.hash_value2_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        self.verify_button = ttk.Button(root, text="Verify", command=self.verify, state='disabled')
        self.verify_button.grid(row=2, column=1, padx=10, pady=10, rowspan=2, sticky='ew')

        self.dashboard_label = tk.Label(root, font=('Arial', 12), bg='#334257')
        self.dashboard_label.grid(row=5, column=0, columnspan=2, pady=10, sticky='e')

        # Adjust window width and set the initial window size and position
        root.geometry("600x350")  # Increased width to accommodate two columns

    def import_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Import")
        if file_path:
            file_name = os.path.basename(file_path)
            self.file_path.set(file_path)
            self.generate_button.config(state='normal')
            self.verify_button.config(state='disabled')
            self.save_hash_button.config(state='disabled')
            self.display_message(f"File '{file_name}' Import Successful!", "info")

    def generate_hash(self):
        file_path = self.file_path.get()
        if file_path:
            self.hash_value1.set(self.calculate_hash(file_path, algorithm="sha256"))
            self.verify_button.config(state='normal')
            self.save_hash_button.config(state='normal')

    def save_hash(self):
        hash_value1 = self.hash_value1.get()
        if hash_value1:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(hash_value1)
                messagebox.showinfo("Save Hash", "Hash value saved successfully.")

    def verify(self):
        hash_value1 = self.hash_value1.get()
        hash_value2 = self.hash_value2.get()

        if not hash_value2:
            self.display_message("Please enter a value in 'Hash Value Two' field.", "error")
        elif hash_value1 == hash_value2:
            self.display_message("File Integrity Checked, File is Okay\n\nThank you for using the Hash Verifier", "success")
        else:
            self.display_message("File Integrity Breached, File has been tampered with\n\nThank you for using the Hash Verifier", "error")

    def display_message(self, message, status="info"):
        self.dashboard_label.config(text=message)
        if status == "success":
            self.dashboard_label.config(foreground='#00FF00')  # Green for success
        elif status == "error":
            self.dashboard_label.config(foreground='#FF0000')  # Red for error
        else:
            self.dashboard_label.config(foreground='#EEEEEE')  # Default color

    @staticmethod
    def calculate_hash(file_path, algorithm="sha256", buffer_size=65536):
        hasher = hashlib.new(algorithm)
        with open(file_path, 'rb') as file:
            while chunk := file.read(buffer_size):
                hasher.update(chunk)
        return hasher.hexdigest()

if __name__ == "__main__":
    root = tk.Tk()
    app = HashVerifierApp(root)
    root.mainloop()
