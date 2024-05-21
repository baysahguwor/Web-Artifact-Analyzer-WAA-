import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
from Home import CaseInformation

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Artifacts Analyzer (WAA)")
        self.root.state("zoomed")  # Adjust as needed or use 'zoomed' for full screen

        # Configure style for the tabs and frames
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('Helvetica', 10, 'bold'), padding=[20, 10], relief='flat')
        self.style.configure('TFrame', background='#f0f0f0', borderwidth=5, relief='groove')
        self.style.configure('Custom.TButton', font=('Helvetica', 12, 'bold'), background='blue', foreground='white')

        self.setup_ui()

    def setup_ui(self):
        self.logo_frame = tk.Frame(self.root, bg='gray')  # Background for visual distinction
        self.logo_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 2))

        # Visual separator
        self.divider_frame = tk.Frame(self.root, bg='black', width=2)
        self.divider_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.tab_frame = tk.Frame(self.root)
        self.tab_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Placeholder for logo; ensure the path to your actual image is correct
        self.logo_image = tk.PhotoImage(file="logo.png")  # Make sure this path is correct or comment this out if the image is not available
        self.logo_label = tk.Label(self.logo_frame, image=self.logo_image, bg='gray')
        self.logo_label.pack(side=tk.TOP, pady=20)

        # As an alternative to not having an actual image loaded, let's use a text label
        self.logo_text_label = tk.Label(self.logo_frame, text="WAA Version 1.0", bg='gray', fg='white', font=("Helvetica", 16))
        self.logo_text_label.pack(side=tk.TOP, pady=20)
        #self.logo_text_label.pack(side=tk.BOTTOM, pady=20))

        # Version information under the logo
        #self.version_label = tk.Label(self.logo_frame, text="Version 1", bg='gray', fg='white', font=("Helvetica", 10))
        #self.version_label.pack(side=tk.BOTTOM, pady=(0, 20))

        self.tabControl = ttk.Notebook(self.tab_frame)
        self.tabControl.pack(expand=1, fill="both")

        self.setup_tabs()

    def setup_tabs(self):
        # Applying padding to frames to provide internal spacing
        self.home_tab = ttk.Frame(self.tabControl, padding=10)
        self.tabControl.add(self.home_tab, text="Home")
        self.populate_home_tab()

        self.developers_tab = ttk.Frame(self.tabControl, padding=10)
        self.tabControl.add(self.developers_tab, text="See Developers")
        self.populate_developers_tab()

        self.disclaimer_tab = ttk.Frame(self.tabControl, padding=10)
        self.tabControl.add(self.disclaimer_tab, text="Disclaimer")
        self.populate_disclaimer_tab()

    def populate_home_tab(self):
        self.create_case_button = tk.Button(self.home_tab, text="Create Case", command=self.create_case, font=('Helvetica', 12, 'bold'), bg='blue', fg='white')
        self.create_case_button.pack(pady=(200, 10), ipadx=290, ipady=20)

        button_row_1 = tk.Frame(self.home_tab)
        button_row_1.pack(pady=5)
        button_row_2 = tk.Frame(self.home_tab)
        button_row_2.pack(pady=5)

        button_configs = [
            ("Analyzer", self.open_analyzer),
            ("Encrypt File", self.encrypt_file),
            ("Decrypt File", self.decrypt_file),
            ("Hash Verifier", self.hash_verifier),
        ]

        for i, (text, command) in enumerate(button_configs[:2]):
            tk.Button(button_row_1, text=text, command=command, padx=110, pady=15, width=15, bg='darkgray', fg='black').pack(side=tk.LEFT, padx=10)
        
        for i, (text, command) in enumerate(button_configs[2:]):
            tk.Button(button_row_2, text=text, command=command, padx=110, pady=15, width=15, bg='darkgray', fg='black').pack(side=tk.LEFT, padx=10)

    def create_case(self):
        subprocess.run(["python", "home.py"])
        #print("Create Case Module")
        

    def open_analyzer(self):
        subprocess.run(["python", "analyzer.py"])

    def encrypt_file(self):
        subprocess.run(["python", "encrypt.py"])

    def decrypt_file(self):
        subprocess.run(["python", "decrypt.py"])

    def hash_verifier(self):
        subprocess.run(["python", "hash_verifier.py"])

    def populate_developers_tab(self):
        developers_label = tk.Label(self.developers_tab, text="Meet our Developers:", font=("Helvetica", 24), bg='white')
        developers_label.pack(pady=10)

        developers_list = [
            "Andrew J. Diggs",
            "Baysah Guwor",
            "Enoch Success Boakai"
        ]

        for developer in developers_list:
            tk.Label(self.developers_tab, text=developer, font=("Helvetica", 18), bg='white').pack(pady=5)

    def populate_disclaimer_tab(self):
        disclaimer_text = """

        ================================================================================
        Licensed under MIT LICENSE:

        
        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        
        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
        
        IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
        ================================================================================
        """ 
        
        # Your disclaimer text here
        text_widget = scrolledtext.ScrolledText(self.disclaimer_tab, wrap=tk.WORD, width=80, height=20)
        text_widget.insert(tk.END, disclaimer_text)
        text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text_widget.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
