"""
==========================================================
Hospital Inventory Analytics System (HIAS)
Audit Module - Utility Functions
Version : 2.0
Author  : Mangesh Ukey
==========================================================
"""

import os
import gc
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd

# ==========================================================
# CONFIGURATION
# ==========================================================

APP_NAME = "Hospital Inventory Analytics System"
APP_VERSION = "2.0"

# Processing
CHUNK_SIZE = 100000

# Excel
MAX_ROWS_PER_SHEET = 1048576

# Folder Structure
BASE_DIR = Path.cwd()

INPUT_FOLDER = BASE_DIR / "Input"
OUTPUT_FOLDER = BASE_DIR / "Output"
LOG_FOLDER = BASE_DIR / "Logs"
TEMP_FOLDER = BASE_DIR / "Temp"

# Create folders automatically
for folder in [INPUT_FOLDER, OUTPUT_FOLDER, LOG_FOLDER, TEMP_FOLDER]:
    folder.mkdir(parents=True, exist_ok=True)

# Date Format
DATE_FORMAT = "%d-%m-%Y"
TIME_FORMAT = "%H:%M:%S"

# Today's Log Folder
TODAY = datetime.now().strftime("%Y-%m-%d")
TODAY_LOG_FOLDER = LOG_FOLDER / TODAY
TODAY_LOG_FOLDER.mkdir(parents=True, exist_ok=True)

# Log Files
APPLICATION_LOG = TODAY_LOG_FOLDER / "Application.log"
ERROR_LOG = TODAY_LOG_FOLDER / "Error.log"
PERFORMANCE_LOG = TODAY_LOG_FOLDER / "Performance.log"
AUDIT_LOG = TODAY_LOG_FOLDER / "Audit.log"


# ==========================================================
# LOGGER
# ==========================================================

def get_logger(name="HIAS"):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S"
    )

    app_handler = logging.FileHandler(APPLICATION_LOG, encoding="utf-8")
    app_handler.setFormatter(formatter)

    logger.addHandler(app_handler)

    return logger


logger = get_logger()


# ==========================================================
# LOG FUNCTIONS
# ==========================================================

def log_info(message):
    logger.info(message)


def log_warning(message):
    logger.warning(message)


def log_error(message):
    logger.error(message)


log_info("=" * 70)
log_info(f"{APP_NAME} Started")
log_info(f"Version : {APP_VERSION}")
log_info("=" * 70)
# ==========================================================
# PERFORMANCE TIMER
# ==========================================================

class PerformanceTimer:
    """
    Measures execution time of any process.
    """

    def __init__(self, process_name: str):
        self.process_name = process_name
        self.start_time = None

    def start(self):
        self.start_time = time.perf_counter()
        log_info(f"[START] {self.process_name}")

    def stop(self):
        if self.start_time is None:
            return

        elapsed = time.perf_counter() - self.start_time

        message = (
            f"[COMPLETED] {self.process_name} "
            f"| Time : {elapsed:.2f} Seconds"
        )

        log_info(message)

        with open(PERFORMANCE_LOG, "a", encoding="utf-8") as f:
            f.write(
                f"{datetime.now():%d-%m-%Y %H:%M:%S} | {message}\n"
            )


# ==========================================================
# MEMORY MANAGEMENT
# ==========================================================

def release_memory(*objects):
    """
    Release memory after processing large DataFrames.
    """

    for obj in objects:
        try:
            del obj
        except Exception:
            pass

    gc.collect()


# ==========================================================
# DATA CLEANING
# ==========================================================

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize all column names.
    """

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.upper()
    )

    return df


# ==========================================================
# SAFE CONVERSIONS
# ==========================================================

def safe_to_numeric(series):
    """
    Convert values safely into numeric.
    """

    return pd.to_numeric(series, errors="coerce").fillna(0)


def safe_to_datetime(series):
    """
    Convert values safely into datetime.
    """

    return pd.to_datetime(series, errors="coerce")


# ==========================================================
# REQUIRED COLUMN VALIDATION
# ==========================================================

def validate_columns(df: pd.DataFrame, required_columns: list):
    """
    Validate required columns.
    """

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing Columns : " + ", ".join(missing)
        )

    return True


# ==========================================================
# DUPLICATE COLUMN CHECK
# ==========================================================

def check_duplicate_columns(df: pd.DataFrame):

    duplicate_cols = (
        df.columns[df.columns.duplicated()]
        .tolist()
    )

    if duplicate_cols:

        log_warning(
            f"Duplicate Columns Found : {duplicate_cols}"
        )

    return duplicate_cols


# ==========================================================
# DATAFRAME INFORMATION
# ==========================================================

def dataframe_info(df: pd.DataFrame, title="DataFrame"):

    rows, cols = df.shape

    log_info(
        f"{title} | Rows : {rows:,} | Columns : {cols}"
    )

    return rows, cols