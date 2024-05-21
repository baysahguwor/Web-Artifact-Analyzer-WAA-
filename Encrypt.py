import tkinter as tk
from tkinter import filedialog, ttk  # ttk for styled widgets
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
import os

class EncryptFileApp:
    def __init__(self, parent):
        parent.title("Encrypt File")  # Updated title for clarity

        # Style Configuration
        parent.configure(bg='#334257')  # Background color
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10, 'bold'), borderwidth='4')
        style.configure('TLabel', background='#334257', foreground='#EEEEEE', font=('Arial', 10))
        style.map('TButton', foreground=[('!active', '#EEEEEE'), ('active', '#FFD700')], background=[('!active','#476072'), ('active', '#FFA500')])

        # Variables
        self.file_path = ""
        self.password = tk.StringVar()

        # GUI Elements
        self.import_button = ttk.Button(parent, text="Import File", command=self.import_file)
        self.import_button.pack(pady=20, padx=20)

        self.password_label = ttk.Label(parent, text="Enter Encryption Key:")
        self.password_label.pack(pady=2)

        self.password_entry = ttk.Entry(parent, show="*", textvariable=self.password)
        self.password_entry.pack(pady=2, padx=20)

        self.dashboard_label = ttk.Label(parent, text="")
        self.dashboard_label.pack(pady=10)

        self.encrypt_button = ttk.Button(parent, text="Encrypt", command=self.encrypt_file)
        self.encrypt_button.pack(pady=10, padx=20)

        # Set the initial window size and style
        parent.geometry("500x300")

    def import_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Import")
        if file_path:
            self.file_path = file_path
            self.dashboard_label.config(text=f"File '{os.path.basename(file_path)}' Imported Successfully!")

    def encrypt_file(self):
        if self.file_path and self.password.get():
            try:
                with open(self.file_path, 'rb') as file:
                    data = file.read()

                    # Derive key from password using PBKDF2
                    key = PBKDF2(self.password.get(), b'', dkLen=32, count=1000000)

                    # Generate a random IV
                    iv = os.urandom(16)

                    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
                    ciphertext = cipher.encrypt(pad(data, AES.block_size))

                # Save encrypted data and IV back to the original file
                with open(self.file_path, 'wb') as encrypted_file:
                    encrypted_file.write(iv + ciphertext)

                self.dashboard_label.config(text="File Encrypted Successfully!")
            except Exception as e:
                self.dashboard_label.config(text=f"Error: {str(e)}")
        else:
            self.dashboard_label.config(text="Please import a file and enter an encryption key.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptFileApp(root)
    root.mainloop()
