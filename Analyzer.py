import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import sqlite3
import pandas as pd  # You'll need pandas for exporting to Excel

class DBFileImporterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite Viewer")
        self.root.state('zoomed')  # Open in zoomed mode

        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10, "bold"), background="#E1E1E1")
        self.style.configure("TLabel", font=("Arial", 10), background="#D3D3D3", relief="flat")
        self.style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))  # Custom Treeview style
        self.style.configure("Treeview.Heading", font=('Calibri', 13, 'bold'))  # Heading font
        self.style.map('Treeview', background=[('selected', '#347083')])  # Selection color

        # Enhanced GUI
        self.root.configure(bg="#F0F0F0")  # Background color of the root window

        # File path variable
        self.file_path = tk.StringVar()

        # Create GUI elements with updated styles
        button_frame = tk.Frame(root, bg="#F0F0F0")
        button_frame.pack(side="top", fill="x", padx=5, pady=5)

        self.import_db_button = ttk.Button(button_frame, text="Import .db File", command=self.import_db_file)
        self.import_db_button.pack(side="left", padx=5)

        self.db_info_label = ttk.Label(button_frame, text="", anchor="w", justify="left")
        self.db_info_label.pack(side="left", fill="x", expand=True, padx=5)

        # Search field
        self.search_entry = ttk.Entry(button_frame)
        self.search_entry.pack(side="left", padx=5)

        # Execute button for search
        self.execute_button = ttk.Button(button_frame, text="Execute", command=self.execute_search)
        self.execute_button.pack(side="left", padx=5)

        # Button for exporting selected rows
        self.export_button = ttk.Button(button_frame, text="Export Selected to Excel", command=self.export_to_excel)
        self.export_button.pack(side="right", padx=5)

        # Create Treeview for displaying tabular data
        self.tree = ttk.Treeview(root, selectmode="browse")
        self.tree["columns"] = ()  # To be dynamically configured based on the data
        self.tree.pack(side="top", fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.show_table_content)  # Bind selection event

        # Scrollbars for Treeview
        self.tree_scroll = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree_scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        # Create frame to display table content
        self.table_frame = tk.Frame(root, bg="#F0F0F0")
        self.table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Reference to the Treeview widget for table content
        self.table_tree = None

    def import_db_file(self):
        file_path = filedialog.askopenfilename(title="Select .db File to Import", filetypes=[("SQLite Database", "*.db")])
        if file_path:
            self.file_path.set(file_path)
            db_info = self.get_db_info(file_path)
            self.display_db_info(db_info)
            self.configure_treeview_columns(file_path)
            file_name = file_path.split("/")[-1]  # Extract the file name from the path
            self.display_message(f"File '{file_name}' import successful.")

    def get_db_info(self, file_path):
        try:
            connection = sqlite3.connect(file_path)
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_names = cursor.fetchall()
            connection.close()
            return [table[0] for table in table_names]
        except sqlite3.Error as e:
            return f"Error accessing database: {str(e)}"

    def display_db_info(self, db_info):
        self.db_info_label.config(text=f"Database tables: {', '.join(db_info)}")

    def configure_treeview_columns(self, file_path):
        try:
            connection = sqlite3.connect(file_path)
            cursor = connection.cursor()

            # Clear existing columns
            self.tree["columns"] = ()

            # Fetch table names dynamically
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_names = cursor.fetchall()

            # Configure Treeview with table names
            for table_name in table_names:
                self.tree.heading("#0", text="Tables")
                self.tree.insert("", "end", text=table_name[0], values=(table_name[0],))

            connection.close()
        except sqlite3.Error as e:
            print(f"Error configuring Treeview columns: {str(e)}")

    def show_table_content(self, event):
        selected_item = self.tree.selection()[0]
        table_name = self.tree.item(selected_item, "text")
        file_path = self.file_path.get()

        if table_name and file_path:
            try:
                connection = sqlite3.connect(file_path)
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM {table_name};")
                data = cursor.fetchall()
                connection.close()

                # Display table content below
                if data:
                    # Clear previous content
                    for widget in self.table_frame.winfo_children():
                        widget.destroy()

                    # Set up table frame
                    table_label = ttk.Label(self.table_frame, text=f"Table: {table_name}")
                    table_label.pack(side="top")

                    # Create Treeview to display table content
                    self.table_tree = ttk.Treeview(self.table_frame, selectmode="browse")

                    # Set up columns
                    columns = [i[0] for i in cursor.description]
                    self.table_tree["columns"] = columns
                    self.table_tree.heading("#0", text="Index")
                    for col in columns:
                        self.table_tree.heading(col, text=col)

                    # Insert data
                    for i, row in enumerate(data):
                        self.table_tree.insert("", "end", text=i, values=row)

                    self.table_tree.pack(side="top", fill="both", expand=True)
            except sqlite3.Error as e:
                print(f"Error accessing table: {str(e)}")

    def execute_search(self):
        search_text = self.search_entry.get().lower()  # Get search text
        if search_text and self.table_tree:
            # Clear previous selection
            self.table_tree.selection_remove(self.table_tree.selection())
            found_items = []
            # Iterate over table rows to search for the text
            for item in self.table_tree.get_children():
                values = self.table_tree.item(item, "values")
                if any(search_text in str(value).lower() for value in values):
                    self.table_tree.selection_add(item)
                    found_items.append(item)
            # If items found, scroll to the first one
            if found_items:
                self.table_tree.see(found_items[0])
        else:
            messagebox.showwarning("Search Error", "No table content to search.")

    def export_to_excel(self):
        selected_items = self.table_tree.selection()
        data = [self.table_tree.item(item, "values") for item in selected_items]
        if data:
            columns = self.table_tree["columns"]
            df = pd.DataFrame(data, columns=columns)
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Export Success", f"Data exported successfully to {file_path}")
        else:
            messagebox.showwarning("Export Error", "No rows selected for export.")

    def display_message(self, message):
        messagebox.showinfo("Import Success", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = DBFileImporterApp(root)
    root.mainloop()
