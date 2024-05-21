import os
import tkinter as tk
from tkinter import ttk
import sqlite3
from fpdf import FPDF
from tkinter import messagebox
import subprocess
import winreg

class ReportApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Report Generator")
        self.master.geometry("1500x700")

        self.progress_label = ttk.Label(self.master, text="Ready to generate report", foreground="black")
        self.progress_label.pack(pady=10)

        self.export_to_pdf_button = ttk.Button(self.master, text="Export to PDF", command=self.export_to_pdf)
        self.export_to_pdf_button.pack(pady=10)
        self.export_to_pdf_button.config(state="disabled")

        self.output_text = tk.Text(self.master, wrap="word")
        self.output_text.pack(expand=True, fill="both")

        self.get_system_info_and_browsers()  # Generate report without threading

    def get_system_info_and_browsers(self):
        # Simulate gathering case information
        self.progress_label.config(text="Gathering Case information...", foreground="black")

        system_info = self.get_system_info()
        installed_browsers = self.get_installed_browsers()
        examiner_info = self.get_examiner_info()

        # Display "All done" when all information is gathered
        self.progress_label.config(text="All done", foreground="black")

        self.display_report(system_info, installed_browsers, examiner_info)

        # Enable export to PDF button after generating the report
        self.export_to_pdf_button.config(state="normal")

    def get_system_info(self):
        system_info = {}
        try:
            output = subprocess.check_output("systeminfo", shell=True, universal_newlines=True)
            for line in output.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    system_info[key.strip()] = value.strip()
        except Exception as e:
            print("Error:", e)

        return system_info

    def get_installed_browsers(self):
        installed_browsers = []
        browser_key = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, browser_key) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if "chrome" in display_name.lower() and "Chrome" not in installed_browsers:
                                installed_browsers.append("Chrome")
                            elif "firefox" in display_name.lower() and "Firefox" not in installed_browsers:
                                installed_browsers.append("Firefox")
                            elif "safari" in display_name.lower() and "Safari" not in installed_browsers:
                                installed_browsers.append("Safari")
                            elif "edge" in display_name.lower() and "Edge" not in installed_browsers:
                                installed_browsers.append("Edge")
                            elif "opera" in display_name.lower() and "Opera" not in installed_browsers:
                                installed_browsers.append("Opera")
                        except FileNotFoundError:
                            pass
        except Exception as e:
            print("Error:", e)

        # Check additional location for Firefox
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe") as key:
                firefox_path = winreg.QueryValueEx(key, None)[0]
                if firefox_path and "Firefox" not in installed_browsers:
                    installed_browsers.append("Firefox")
        except Exception as e:
            pass

        return installed_browsers

    def get_examiner_info(self):
        try:
            db_path = os.path.join("Evidence", "database.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Examiner")
            examiner_info = cursor.fetchall()
            conn.close()
            return examiner_info
        except Exception as e:
            print("Error:", e)
            return []

    def display_report(self, system_info, installed_browsers, examiner_info):
        report_text = ""

        # Add "Examiner Information" section
        report_text += "Examiner Information:\n"
        if examiner_info:
            for row in examiner_info:
                report_text += "    ".join(map(str, row)) + "\n"
        else:
            report_text += "No examiner information found.\n"
        report_text += "\n"

        # Add "System Information" section
        report_text += "System Information:\n"
        for key, value in system_info.items():
            report_text += f"{key}: {value}\n"
        report_text += "\n"

        # Add "Installed Browsers" section
        report_text += "Installed Browsers:\n"
        if installed_browsers:
            for browser in installed_browsers:
                report_text += f"    {browser}\n"
        else:
            report_text += "No browsers found.\n"

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, report_text)

    def export_to_pdf(self):
        system_info = self.get_system_info()
        installed_browsers = self.get_installed_browsers()
        examiner_info = self.get_examiner_info()
        report_text = self.generate_report_text(system_info, installed_browsers, examiner_info)
        self.create_pdf(report_text)

    def generate_report_text(self, system_info, installed_browsers, examiner_info):
        report_text = ""

        # Add "Examiner Information" section
        report_text += "Examiner Information:\n"
        if examiner_info:
            for row in examiner_info:
                report_text += "    ".join(map(str, row)) + "\n"
        else:
            report_text += "No examiner information found.\n"
        report_text += "\n"

        # Add "System Information" section
        report_text += "System Information:\n"
        for key, value in system_info.items():
            report_text += f"{key}: {value}\n"
        report_text += "\n"

        # Add "Installed Browsers" section
        report_text += "Installed Browsers:\n"
        if installed_browsers:
            for browser in installed_browsers:
                report_text += f"    {browser}\n"
        else:
            report_text += "No browsers found.\n"

        return report_text

    def create_pdf(self, report_text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add border to the page
        pdf.rect(5.0, 5.0, 200.0, 287.0)

        # Add "WEB ARTIFACTS ANALYZER GENERATED REPORT" text
        pdf.set_font("Arial", size=12, style='B')
        pdf.set_y(10)
        pdf.cell(0, 10, "WEB ARTIFACTS ANALYZER GENERATED REPORT", 0, 1, "C")
        # Add "Copyright at WAA - MU 2024" text
        pdf.cell(0, 10, "Copyright © WAA - MU 2024", 0, 1, "C")

        # Add "Examiner Information" section
        pdf.set_font("Arial", size=18, style='B')
        pdf.cell(200, 10, txt="Examiner Information", ln=True, align="L")
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, report_text.split("System Information:")[0])

        # Add "System Information" section
        pdf.set_font("Arial", size=18, style='B')
        pdf.cell(200, 10, txt="System Information", ln=True, align="L")
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, report_text.split("System Information:")[1].split("Installed Browsers:")[0])

        # Add "Installed Browsers" section
        pdf.set_font("Arial", size=18, style='B')
        pdf.cell(200, 10, txt="Installed Browsers", ln=True, align="L")
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, report_text.split("Installed Browsers:")[1])

        pdf_file = "system_report.pdf"
        pdf.output(pdf_file)
        messagebox.showinfo("Export to PDF", f"Report exported to {pdf_file}")

def main():
    root = tk.Tk()
    app = ReportApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
