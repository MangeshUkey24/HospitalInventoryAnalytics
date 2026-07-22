"""
------------------------------------------------------------
Hospital Inventory Analytics System (HIAS)
Stock Calculation Engine
------------------------------------------------------------
Author : Mangesh Ukey
Version : 1.0
------------------------------------------------------------
"""

import pandas as pd
import logging

class StockEngine:

    def __init__(self,
                 opening_df,
                 purchase_df,
                 sales_df,
                 adjustment_df):

        self.opening = opening_df.copy()
        self.purchase = purchase_df.copy()
        self.sales = sales_df.copy()
        self.adjustment = adjustment_df.copy()

        # Cache for generated reports
        self._daily_stock = None

    # --------------------------------------------------------
    # Standardize Data
    # --------------------------------------------------------
    def prepare(self):

        self.opening["item_name"] = (
            self.opening["item_name"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        self.purchase["item_name"] = (
            self.purchase["item_name"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        self.sales["item_name"] = (
            self.sales["item_name"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        self.adjustment["item_name"] = (
            self.adjustment["item_name"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        self.purchase["date"] = pd.to_datetime(self.purchase["date"])
        self.sales["date"] = pd.to_datetime(self.sales["date"])
        self.adjustment["date"] = pd.to_datetime(self.adjustment["date"])

    # --------------------------------------------------------
    # Daily Stock Report
    # --------------------------------------------------------
    def daily_stock(self):

        # Return cached report if already generated
        if self._daily_stock is not None:
            return self._daily_stock

        self.prepare()

        start_date = min(
            self.purchase["date"].min(),
            self.sales["date"].min(),
            self.adjustment["date"].min()
        )

        end_date = max(
            self.purchase["date"].max(),
            self.sales["date"].max(),
            self.adjustment["date"].max()
        )

        opening_stock = dict(
            zip(
                self.opening["item_name"],
                self.opening["qty"]
            )
        )

        mrp_dict = dict(
            zip(
                self.opening["item_name"],
                self.opening.get("mrp", 0)
            )
        )

        epr_dict = dict(
            zip(
                self.opening["item_name"],
                self.opening.get("epr", 0)
            )
        )

        report = []

        dates = pd.date_range(start_date, end_date)

        for current_date in dates:

            purchase_day = (
                self.purchase[
                    self.purchase["date"] == current_date
                ]
                .groupby("item_name")["qty"]
                .sum()
            )

            sales_day = (
                self.sales[
                    self.sales["date"] == current_date
                ]
                .groupby("item_name")["qty"]
                .sum()
            )

            adjustment_day = (
                self.adjustment[
                    self.adjustment["date"] == current_date
                ]
                .groupby("item_name")["qty"]
                .sum()
            )

            items = set(opening_stock.keys())
            items.update(purchase_day.index)
            items.update(sales_day.index)
            items.update(adjustment_day.index)

            for item in sorted(items):

                opening_qty = opening_stock.get(item, 0)

                purchase_qty = purchase_day.get(item, 0)

                sales_qty = sales_day.get(item, 0)

                adjustment_qty = adjustment_day.get(item, 0)

                closing_qty = (
                    opening_qty
                    + purchase_qty
                    + adjustment_qty
                    - sales_qty
                )

                report.append({

                    "Date": current_date.date(),

                    "Item Name": item,

                    "Opening Qty": opening_qty,

                    "Purchase Qty": purchase_qty,

                    "Sales Qty": sales_qty,

                    "Adjustment Qty": adjustment_qty,

                    "Closing Qty": closing_qty,

                    "MRP": mrp_dict.get(item, 0),

                    "EPR": epr_dict.get(item, 0),

                    "MRP Value": closing_qty * mrp_dict.get(item, 0),

                    "EPR Value": closing_qty * epr_dict.get(item, 0)

                })

                opening_stock[item] = closing_qty

        df = pd.DataFrame(report)

        # Store report in cache
        self._daily_stock = df

        logging.info("Daily Stock Report Generated")

        return self._daily_stock
    # --------------------------------------------------------
    # Weekly Report
    # --------------------------------------------------------
    def weekly_stock(self):

        daily = self.daily_stock()

        daily["Date"] = pd.to_datetime(daily["Date"])

        daily["Week"] = (
            daily["Date"]
            .dt.strftime("%Y-W%U")
        )

        weekly = (

            daily

            .groupby(

                ["Week",
                 "Item Name"],

                as_index=False

            )

            .agg({

                "Opening Qty": "first",

                "Purchase Qty": "sum",

                "Sales Qty": "sum",

                "Adjustment Qty": "sum",

                "Closing Qty": "last",

                "MRP Value": "last",

                "EPR Value": "last"

            })

        )

        logging.info("Weekly Stock Report Generated")

        return weekly

    # --------------------------------------------------------
    # Monthly Report
    # --------------------------------------------------------
    def monthly_stock(self):

        daily = self.daily_stock()

        daily["Date"] = pd.to_datetime(daily["Date"])

        daily["Month"] = (
            daily["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly = (

            daily

            .groupby(

                ["Month",
                 "Item Name"],

                as_index=False

            )

            .agg({

                "Opening Qty": "first",

                "Purchase Qty": "sum",

                "Sales Qty": "sum",

                "Adjustment Qty": "sum",

                "Closing Qty": "last",

                "MRP Value": "last",

                "EPR Value": "last"

            })

        )

        logging.info("Monthly Stock Report Generated")

        return monthly

    # --------------------------------------------------------
    # Item Ledger
    # --------------------------------------------------------
    def item_ledger(self):

        return self.daily_stock()

    # --------------------------------------------------------
    # Negative Stock
    # --------------------------------------------------------
    def negative_stock(self):

        df = self.daily_stock()

        return df[df["Closing Qty"] < 0]

    # --------------------------------------------------------
    # Zero Stock
    # --------------------------------------------------------
    def zero_stock(self):

        df = self.daily_stock()

        return df[df["Closing Qty"] == 0]

    # --------------------------------------------------------
    # Slow Moving
    # --------------------------------------------------------
    def slow_moving(self, days=90):

        latest = self.sales["date"].max()

        last_sale = (

            self.sales

            .groupby("item_name")["date"]

            .max()

            .reset_index()

        )

        last_sale["Days"] = (

            latest

            - last_sale["date"]

        ).dt.days

        return last_sale[last_sale["Days"] >= days]

    # --------------------------------------------------------
    # Stock Summary
    # --------------------------------------------------------
    def summary(self):

        daily = self.daily_stock()

        return {

            "Total Items":
                daily["Item Name"].nunique(),

            "Total Closing Qty":
                daily["Closing Qty"].sum(),

            "Total MRP Value":
                daily["MRP Value"].sum(),

            "Total EPR Value":
                daily["EPR Value"].sum()

        }