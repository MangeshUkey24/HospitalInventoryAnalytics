"""
------------------------------------------------------------
Hospital Inventory Analytics System (HIAS)
Application Settings
------------------------------------------------------------
Author  : Mangesh Ukey
Version : 1.0
------------------------------------------------------------
"""

from pathlib import Path
import customtkinter as ctk


class Settings:
    """
    Global application settings.
    """

    # ========================================================
    # Application Information
    # ========================================================
    APP_NAME = "Hospital Inventory Analytics System"

    APP_SHORT_NAME = "HIAS"

    VERSION = "1.0"

    AUTHOR = "Mangesh Ukey"

    COMPANY = "Healthcare IT Solutions"

    # ========================================================
    # Window Settings
    # ========================================================
    WINDOW_WIDTH = 1200

    WINDOW_HEIGHT = 750

    MIN_WIDTH = 1000

    MIN_HEIGHT = 650

    APPEARANCE_MODE = "System"
    # Options:
    # System
    # Light
    # Dark

    COLOR_THEME = "blue"

    # ========================================================
    # Folder Structure
    # ========================================================
    BASE_DIR = Path(__file__).resolve().parent

    INPUT_DIR = BASE_DIR / "Input"

    OUTPUT_DIR = BASE_DIR / "Output"

    CONFIG_DIR = BASE_DIR / "Config"

    LOG_DIR = BASE_DIR / "Logs"

    ASSET_DIR = BASE_DIR / "Assets"

    TEMP_DIR = BASE_DIR / "Temp"

    TEST_DIR = BASE_DIR / "Tests"

    DATABASE_DIR = BASE_DIR / "Database"

    # ========================================================
    # Files
    # ========================================================
    CONFIG_FILE = CONFIG_DIR / "hospital_config.json"

    LOG_FILE = LOG_DIR / "application.log"

    DATABASE_FILE = DATABASE_DIR / "hias.db"

    LOGO_FILE = ASSET_DIR / "logo.png"

    # ========================================================
    # Excel
    # ========================================================
    FREEZE_PANES = "A5"

    HEADER_ROW = 4

    DATE_FORMAT = "%d-%m-%Y"

    DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"

    AUTO_FILTER = True

    AUTO_FIT_COLUMNS = True

    # ========================================================
    # Report Names
    # ========================================================
    DAILY_REPORT = "Daily Stock"

    WEEKLY_REPORT = "Weekly Stock"

    MONTHLY_REPORT = "Monthly Stock"

    LEDGER_REPORT = "Item Ledger"

    NEGATIVE_REPORT = "Negative Stock"

    ZERO_REPORT = "Zero Stock"

    SLOW_MOVING_REPORT = "Slow Moving"

    DASHBOARD_REPORT = "Dashboard"

    SUMMARY_REPORT = "Summary"

    # ========================================================
    # Fonts
    # ========================================================
    TITLE_FONT = ("Arial", 20, "bold")

    HEADER_FONT = ("Calibri", 11, "bold")

    NORMAL_FONT = ("Calibri", 10)

    BUTTON_FONT = ("Arial", 12, "bold")

    # ========================================================
    # Colors
    # ========================================================
    PRIMARY_COLOR = "1F4E78"

    SUCCESS_COLOR = "008000"

    WARNING_COLOR = "FFC000"

    ERROR_COLOR = "FF0000"

    HEADER_TEXT = "FFFFFF"

    # ========================================================
    # Dashboard
    # ========================================================
    CHART_WIDTH = 500

    CHART_HEIGHT = 300

    TOP_ITEMS = 10

    # ========================================================
    # Processing
    # ========================================================
    MAX_THREADS = 4

    CHUNK_SIZE = 50000

    ENABLE_LOGGING = True

    ENABLE_DATABASE = True

    # ========================================================
    # Stock Formula
    # ========================================================
    STOCK_FORMULA = (
        "Closing = Opening + Purchase + Adjustment - Sales"
    )

    # ========================================================
    # Create Required Folders
    # ========================================================
    @staticmethod
    def create_folders():

        folders = [

            Settings.INPUT_DIR,
            Settings.OUTPUT_DIR,
            Settings.CONFIG_DIR,
            Settings.LOG_DIR,
            Settings.ASSET_DIR,
            Settings.TEMP_DIR,
            Settings.TEST_DIR,
            Settings.DATABASE_DIR

        ]

        for folder in folders:

            folder.mkdir(
                parents=True,
                exist_ok=True
            )

    # ========================================================
    # Apply Theme
    # ========================================================
    @staticmethod
    def apply_theme():

        ctk.set_appearance_mode(
            Settings.APPEARANCE_MODE
        )

        ctk.set_default_color_theme(
            Settings.COLOR_THEME
        )