"""
------------------------------------------------------------
Hospital Inventory Analytics System (HIAS)
SQLite Database Module
------------------------------------------------------------
Author : Mangesh Ukey
Version : 1.0
------------------------------------------------------------
"""

import sqlite3
import pandas as pd
from pathlib import Path


class DatabaseManager:

    def __init__(self, db_path="Database/hias.db"):

        self.db_path = Path(db_path)

        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)

        self.cursor = self.connection.cursor()

        self.create_tables()

    # --------------------------------------------------------
    # Create Tables
    # --------------------------------------------------------
    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS opening_stock(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            item_name TEXT,

            qty REAL,

            mrp REAL,

            epr REAL

        )

        """)

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS purchase(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            txn_date TEXT,

            item_name TEXT,

            qty REAL,

            mrp REAL,

            epr REAL

        )

        """)

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS sales(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            txn_date TEXT,

            item_name TEXT,

            qty REAL,

            mrp REAL,

            epr REAL

        )

        """)

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS adjustment(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            txn_date TEXT,

            item_name TEXT,

            qty REAL,

            adjustment_type TEXT

        )

        """)

        self.connection.commit()

    # --------------------------------------------------------
    # Clear Table
    # --------------------------------------------------------
    def clear_table(self, table_name):

        self.cursor.execute(f"DELETE FROM {table_name}")

        self.connection.commit()

    # --------------------------------------------------------
    # Insert DataFrame
    # --------------------------------------------------------
    def insert_dataframe(self, table_name, dataframe):

        dataframe.to_sql(

            table_name,

            self.connection,

            if_exists="append",

            index=False

        )

    # --------------------------------------------------------
    # Read Table
    # --------------------------------------------------------
    def read_table(self, table_name):

        query = f"SELECT * FROM {table_name}"

        return pd.read_sql(query, self.connection)

    # --------------------------------------------------------
    # Execute Query
    # --------------------------------------------------------
    def execute(self, query, params=None):

        if params is None:
            params = ()

        self.cursor.execute(query, params)

        self.connection.commit()

    # --------------------------------------------------------
    # Fetch Query
    # --------------------------------------------------------
    def fetch_dataframe(self, query, params=None):

        if params is None:
            params = ()

        return pd.read_sql_query(
            query,
            self.connection,
            params=params
        )

    # --------------------------------------------------------
    # Item Wise Stock
    # --------------------------------------------------------
    def get_opening_stock(self):

        query = """

        SELECT

            item_name,

            SUM(qty) AS opening_qty,

            AVG(mrp) AS mrp,

            AVG(epr) AS epr

        FROM opening_stock

        GROUP BY item_name

        ORDER BY item_name

        """

        return self.fetch_dataframe(query)

    # --------------------------------------------------------
    # Purchase Summary
    # --------------------------------------------------------
    def get_purchase_summary(self):

        query = """

        SELECT

            txn_date,

            item_name,

            SUM(qty) purchase_qty

        FROM purchase

        GROUP BY txn_date,item_name

        """

        return self.fetch_dataframe(query)

    # --------------------------------------------------------
    # Sales Summary
    # --------------------------------------------------------
    def get_sales_summary(self):

        query = """

        SELECT

            txn_date,

            item_name,

            SUM(qty) sales_qty

        FROM sales

        GROUP BY txn_date,item_name

        """

        return self.fetch_dataframe(query)

    # --------------------------------------------------------
    # Adjustment Summary
    # --------------------------------------------------------
    def get_adjustment_summary(self):

        query = """

        SELECT

            txn_date,

            item_name,

            SUM(qty) adjustment_qty

        FROM adjustment

        GROUP BY txn_date,item_name

        """

        return self.fetch_dataframe(query)

    # --------------------------------------------------------
    # Close Database
    # --------------------------------------------------------
    def close(self):

        self.connection.close()