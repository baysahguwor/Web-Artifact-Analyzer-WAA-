import tkinter as tk
from tkinter import filedialog, ttk  # ttk for styled widgets
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
import os

class DecryptFileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Decrypt File")

        # Style Configuration
        root.configure(bg='#334257')  # Background color
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10, 'bold'), borderwidth='4')
        style.configure('TLabel', background='#334257', foreground='#EEEEEE', font=('Arial', 10))
        style.map('TButton', foreground=[('!active', '#EEEEEE'), ('active', '#FFD700')], background=[('!active','#476072'), ('active', '#FFA500')])

        # Variables
        self.file_path = ""
        self.password = tk.StringVar()

        # GUI Elements
        self.import_button = ttk.Button(root, text="Import File", command=self.import_file)
        self.import_button.pack(pady=10, padx=20)

        self.password_label = ttk.Label(root, text="Enter Decryption Key:")
        self.password_label.pack(pady=2)

        self.password_entry = ttk.Entry(root, show="*", textvariable=self.password)
        self.password_entry.pack(pady=2, padx=20)

        self.dashboard_label = ttk.Label(root, text="")
        self.dashboard_label.pack(pady=10)

        self.decrypt_button = ttk.Button(root, text="Decrypt", command=self.decrypt_file)
        self.decrypt_button.pack(pady=10, padx=20)

        # Adjust window position to the center of the screen
        root.geometry("500x300+{}+{}".format(root.winfo_screenwidth() // 2 - 250, root.winfo_screenheight() // 2 - 150))

    def import_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Import")
        if file_path:
            self.file_path = file_path
            self.dashboard_label.config(text=f"File '{os.path.basename(file_path)}' Imported Successfully!")

    def decrypt_file(self):
        if self.file_path and self.password.get():
            try:
                with open(self.file_path, 'rb') as file:
                    data = file.read()

                    # Derive key from password using PBKDF2
                    key = PBKDF2(self.password.get(), b'', dkLen=32, count=1000000)

                    # Extract IV and encrypted data
                    iv, ciphertext = data[:16], data[16:]

                    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
                    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

                # Save decrypted data back to the original file
                with open(self.file_path, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)

                self.dashboard_label.config(text="File Decrypted Successfully!")
            except Exception as e:
                self.dashboard_label.config(text=f"Error: {str(e)}")
        else:
            self.dashboard_label.config(text="Please import a file and enter a decryption key.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DecryptFileApp(root)
    root.mainloop()
