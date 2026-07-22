"""
------------------------------------------------------------
Hospital Inventory Analytics System (HIAS)
Excel Reader Module
------------------------------------------------------------
Author  : Mangesh Ukey
Version : 2.0
------------------------------------------------------------
"""

from pathlib import Path
import pandas as pd

from config_loader import ConfigLoader
from logger import AppLogger


class ExcelReader:

    def __init__(self):

        self.logger = AppLogger.get_logger()
        self.config = ConfigLoader()

    # --------------------------------------------------------
    # Read Excel File
    # --------------------------------------------------------
    def read_excel(self, file_path):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found : {file_path}")

        self.logger.info(f"Reading {file_path.name}")

        try:
            df = pd.read_excel(file_path)

        except Exception as e:
            self.logger.exception("Unable to read excel file")
            raise e

        df = self.clean_dataframe(df)

        df = self.config.standardize_columns(df)
 
        print(f"\nFile: {file_path.name}")
        print(df.columns.tolist())


        df = self.prepare_dataframe(df)

        self.logger.info(
            f"{file_path.name} : {len(df)} rows imported"
        )

        return df

    # --------------------------------------------------------
    # Clean Data
    # --------------------------------------------------------
    def clean_dataframe(self, df):

        df = df.dropna(how="all")

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        df = df.drop_duplicates()

        df.reset_index(drop=True, inplace=True)

        return df

    # --------------------------------------------------------
    # Prepare Data
    # --------------------------------------------------------
    def prepare_dataframe(self, df):

        # Date
        if "date" in df.columns:
            df["date"] = pd.to_datetime(
                df["date"],
                errors="coerce"
            )

        # Quantity
        if "quantity" in df.columns:
            df.rename(columns={"quantity": "qty"}, inplace=True)

        if "qty" in df.columns:
            df["qty"] = pd.to_numeric(
                df["qty"],
                errors="coerce"
            ).fillna(0)

        # MRP
        if "mrp" in df.columns:
            df["mrp"] = pd.to_numeric(
                df["mrp"],
                errors="coerce"
            ).fillna(0)

        # EPR
        if "epr" in df.columns:
            df["epr"] = pd.to_numeric(
                df["epr"],
                errors="coerce"
            ).fillna(0)

        # Item Name
        if "item_name" in df.columns:
            df["item_name"] = (
                df["item_name"]
                .astype(str)
                .str.strip()
                .str.upper()
            )

        return df

    # --------------------------------------------------------
    # Validate Columns
    # --------------------------------------------------------
    def validate_columns(
            self,
            df,
            required_columns
    ):

        missing = [

            column

            for column in required_columns

            if column not in df.columns

        ]

        if missing:

            raise ValueError(

                "Missing required columns : "

                + ", ".join(missing)

            )

    # --------------------------------------------------------
    # Opening Stock
    # --------------------------------------------------------
    def read_opening_stock(self, path):

        df = self.read_excel(path)

        self.validate_columns(

            df,

            [

                "item_name",

                "qty"

            ]

        )

        return df

    # --------------------------------------------------------
    # Purchase
    # --------------------------------------------------------
    def read_purchase(self, path):

        df = self.read_excel(path)

        self.validate_columns(

            df,

            [

                "date",

                "item_name",

                "qty"

            ]

        )

        return df

    # --------------------------------------------------------
    # Sales
    # --------------------------------------------------------
    def read_sales(self, path):

        df = self.read_excel(path)

        self.validate_columns(

            df,

            [

                "date",

                "item_name",

                "qty"

            ]

        )

        return df

     # --------------------------------------------------------
    # Adjustment
    # --------------------------------------------------------
    def read_adjustment(self, path):

        self.logger.info(f"Reading {Path(path).name}")

        df = pd.read_excel(path, header=1)

        df = self.clean_dataframe(df)
        df = self.config.standardize_columns(df)

        # Create qty from Stock Up / Stock Down
        if "STOCK UP" in df.columns and "STOCK DOWN" in df.columns:

            df["qty"] = (
                pd.to_numeric(df["STOCK UP"], errors="coerce").fillna(0)
                -
                pd.to_numeric(df["STOCK DOWN"], errors="coerce").fillna(0)
            )

        df = self.prepare_dataframe(df)

        print(f"\nFile: {Path(path).name}")
        print(df.columns.tolist())

        self.validate_columns(
            df,
            [
                "date",
                "item_name",
                "qty"
            ]
        )

        return df
        raise Exception("Header inspection completed")
    # --------------------------------------------------------
    # Read All Files
    # --------------------------------------------------------
    def read_all(
            self,
            opening_file,
            purchase_file,
            sales_file,
            adjustment_file
    ):

        return {

            "opening": self.read_opening_stock(opening_file),

            "purchase": self.read_purchase(purchase_file),

            "sales": self.read_sales(sales_file),

            "adjustment": self.read_adjustment(adjustment_file)

        }