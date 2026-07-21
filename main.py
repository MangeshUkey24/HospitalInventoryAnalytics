"""
------------------------------------------------------------
Hospital Inventory Analytics System (HIAS)
Main Entry Point
------------------------------------------------------------
Author : Mangesh Ukey
Version: 1.0
Python : 3.12
------------------------------------------------------------
"""

import os
import sys
import logging
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox

# Import Application GUI
from gui import HospitalInventoryApp


# ------------------------------------------------------------
# Create Required Folders
# ------------------------------------------------------------
def create_folders():
    folders = [
        "Input",
        "Output",
        "Logs",
        "Assets"
    ]

    for folder in folders:
        Path(folder).mkdir(exist_ok=True)


# ------------------------------------------------------------
# Logging
# ------------------------------------------------------------
def configure_logging():

    Path("Logs").mkdir(exist_ok=True)

    logging.basicConfig(
        filename="Logs/application.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    logging.info("========================================")
    logging.info("Hospital Inventory Analytics Started")
    logging.info("========================================")


# ------------------------------------------------------------
# Application Theme
# ------------------------------------------------------------
def configure_theme():

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")


# ------------------------------------------------------------
# Global Exception Handler
# ------------------------------------------------------------
def exception_handler(exc_type, exc_value, exc_traceback):

    logging.exception(
        "Unhandled Exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )

    messagebox.showerror(
        "Application Error",
        f"{exc_value}\n\nSee Logs/application.log for details."
    )


# ------------------------------------------------------------
# Start Application
# ------------------------------------------------------------
def start():

    sys.excepthook = exception_handler

    create_folders()

    configure_logging()

    configure_theme()

    logging.info("Launching GUI...")

    app = HospitalInventoryApp()

    app.mainloop()

    logging.info("Application Closed")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
if __name__ == "__main__":

    try:

        start()

    except KeyboardInterrupt:

        logging.warning("Application interrupted by user.")

    except Exception as e:

        logging.exception(e)

        messagebox.showerror(
            "Fatal Error",
            str(e)
        )

        sys.exit(1)