import platform
import psutil
import socket
import getpass
import os
import platform
import subprocess
from datetime import datetime


def check_browser_path(path):
    return os.path.isfile(path)  # Check if the file exists and is a file.

def list_installed_browsers():
    installed_browsers = []

    if platform.system() == "Windows":
        # Expanded common browser paths on Windows
        browsers_paths = {
            "Google Chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "Mozilla Firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            "Microsoft Edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            "Opera": "C:\\Program Files\\Opera\\launcher.exe",
            "Brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        }
        for browser, path in browsers_paths.items():
            if check_browser_path(path):
                installed_browsers.append(browser)

    elif platform.system() in ["Linux", "Darwin"]:
        # Expanded common browser binaries in Unix-like systems
        browsers_bins = ["google-chrome", "firefox", "chromium", "opera", "brave"]
        for bin in browsers_bins:
            try:
                # Check if browser binary is in PATH by attempting to run it with --version argument
                subprocess.run([bin, "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                installed_browsers.append(bin)
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue

    return installed_browsers

# Example usage
#print("Installed Browsers:", list_installed_browsers())
report = list_installed_browsers()
#print(report)


