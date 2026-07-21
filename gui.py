"""
------------------------------------------------------------
Hospital Inventory Analytics System (HIAS)
GUI
------------------------------------------------------------
"""

import os
import customtkinter as ctk
from tkinter import filedialog, messagebox


class HospitalInventoryApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Hospital Inventory Analytics System")
        self.geometry("1000x700")
        self.minsize(900, 650)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # -----------------------------
        # Variables
        # -----------------------------
        self.opening_stock = ctk.StringVar()
        self.purchase_report = ctk.StringVar()
        self.sales_report = ctk.StringVar()
        self.adjustment_report = ctk.StringVar()
        self.output_folder = ctk.StringVar()

        # -----------------------------
        # Title
        # -----------------------------
        title = ctk.CTkLabel(
            self,
            text="Hospital Inventory Analytics System",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=15)

        # -----------------------------
        # File Selection Frame
        # -----------------------------
        file_frame = ctk.CTkFrame(self)
        file_frame.pack(fill="x", padx=20, pady=10)

        self.create_file_row(
            file_frame,
            "Opening Stock Report",
            self.opening_stock,
            0
        )

        self.create_file_row(
            file_frame,
            "Purchase Report",
            self.purchase_report,
            1
        )

        self.create_file_row(
            file_frame,
            "Patient Wise Sales Report",
            self.sales_report,
            2
        )

        self.create_file_row(
            file_frame,
            "Stock Adjustment Report",
            self.adjustment_report,
            3
        )

        self.create_folder_row(
            file_frame,
            "Output Folder",
            self.output_folder,
            4
        )

        # -----------------------------
        # Date Frame
        # -----------------------------
        date_frame = ctk.CTkFrame(self)
        date_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            date_frame,
            text="From Date (DD-MM-YYYY)"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.from_date = ctk.CTkEntry(date_frame, width=180)
        self.from_date.grid(row=0, column=1)

        ctk.CTkLabel(
            date_frame,
            text="To Date (DD-MM-YYYY)"
        ).grid(row=0, column=2, padx=10)

        self.to_date = ctk.CTkEntry(date_frame, width=180)
        self.to_date.grid(row=0, column=3)

        # -----------------------------
        # Generate Button
        # -----------------------------
        self.generate_btn = ctk.CTkButton(
            self,
            text="Generate Reports",
            height=45,
            command=self.generate_reports
        )

        self.generate_btn.pack(pady=15)

        # -----------------------------
        # Progress Bar
        # -----------------------------
        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(fill="x", padx=20)

        self.progress.set(0)

        # -----------------------------
        # Status Label
        # -----------------------------
        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            font=("Arial", 14)
        )

        self.status.pack(pady=8)

        # -----------------------------
        # Log Textbox
        # -----------------------------
        self.log_box = ctk.CTkTextbox(
            self,
            width=900,
            height=250
        )

        self.log_box.pack(fill="both", expand=True, padx=20, pady=15)

        self.log("Application Started.")

    # --------------------------------------------------
    # Create File Row
    # --------------------------------------------------
    def create_file_row(self, parent, label, variable, row):

        ctk.CTkLabel(
            parent,
            text=label,
            width=200,
            anchor="w"
        ).grid(row=row, column=0, padx=10, pady=8)

        entry = ctk.CTkEntry(
            parent,
            textvariable=variable,
            width=550
        )

        entry.grid(row=row, column=1, padx=5)

        button = ctk.CTkButton(
            parent,
            text="Browse",
            width=100,
            command=lambda: self.browse_file(variable)
        )

        button.grid(row=row, column=2, padx=10)

    # --------------------------------------------------
    # Create Folder Row
    # --------------------------------------------------
    def create_folder_row(self, parent, label, variable, row):

        ctk.CTkLabel(
            parent,
            text=label,
            width=200,
            anchor="w"
        ).grid(row=row, column=0, padx=10, pady=8)

        entry = ctk.CTkEntry(
            parent,
            textvariable=variable,
            width=550
        )

        entry.grid(row=row, column=1)

        button = ctk.CTkButton(
            parent,
            text="Browse",
            width=100,
            command=lambda: self.browse_folder(variable)
        )

        button.grid(row=row, column=2, padx=10)

    # --------------------------------------------------
    # Browse File
    # --------------------------------------------------
    def browse_file(self, variable):

        file = filedialog.askopenfilename(
            filetypes=[
                ("Excel Files", "*.xlsx *.xls")
            ]
        )

        if file:
            variable.set(file)

    # --------------------------------------------------
    # Browse Folder
    # --------------------------------------------------
    def browse_folder(self, variable):

        folder = filedialog.askdirectory()

        if folder:
            variable.set(folder)

    # --------------------------------------------------
    # Log
    # --------------------------------------------------
    def log(self, text):

        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    # --------------------------------------------------
    # Validate Inputs
    # --------------------------------------------------
    def validate(self):

        files = [
            self.opening_stock.get(),
            self.purchase_report.get(),
            self.sales_report.get(),
            self.adjustment_report.get(),
            self.output_folder.get()
        ]

        for item in files:
            if item == "":
                return False

        return True

    # --------------------------------------------------
    # Generate Reports
    # --------------------------------------------------
    def generate_reports(self):

        if not self.validate():
            messagebox.showwarning(
                "Missing Information",
                "Please select all required files and output folder."
            )
            return

        self.progress.set(0.10)
        self.status.configure(text="Reading Excel Files...")
        self.log("Reading Opening Stock...")
        self.update()

        # TODO:
        # from excel_reader import read_all_files
        # from stock_engine import calculate_stock
        # from report_generator import generate_reports

        self.progress.set(0.35)
        self.log("Reading Purchase Report...")
        self.update()

        self.progress.set(0.55)
        self.log("Reading Sales Report...")
        self.update()

        self.progress.set(0.75)
        self.log("Reading Adjustment Report...")
        self.update()

        self.progress.set(0.90)
        self.log("Generating Excel Reports...")
        self.update()

        self.progress.set(1.0)
        self.status.configure(text="Completed")
        self.log("Reports Generated Successfully.")

        messagebox.showinfo(
            "Success",
            "Reports generated successfully."
        )