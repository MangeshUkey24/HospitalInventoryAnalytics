"""
------------------------------------------------------------
Hospital Inventory Analytics System (HIAS)
Stock Calculation Engine
------------------------------------------------------------
Author : Mangesh Ukey
Version : 2.0
------------------------------------------------------------
"""

import logging
import pandas as pd


class TransactionEngine:
    """Build a unified transaction list and calculate running stock."""

    def __init__(
        self,
        opening_df=None,
        purchase_df=None,
        sales_df=None,
        adjustment_df=None,
        stock_modify_df=None,
        purchase_return_df=None,
        sales_return_df=None,
        transfer_df=None,
    ):
        self.opening = opening_df.copy() if opening_df is not None else pd.DataFrame(columns=["item_name", "qty"])
        self.purchase = purchase_df.copy() if purchase_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.sales = sales_df.copy() if sales_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.adjustment = adjustment_df.copy() if adjustment_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.stock_modify = stock_modify_df.copy() if stock_modify_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.purchase_return = purchase_return_df.copy() if purchase_return_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.sales_return = sales_return_df.copy() if sales_return_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.transfer = transfer_df.copy() if transfer_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])

        self.transaction_df = pd.DataFrame()
        self.opening_balances = {}

    def _ensure_dataframe(self, df, columns):
        if df is None:
            return pd.DataFrame(columns=columns)

        frame = df.copy()
        for column in columns:
            if column not in frame.columns:
                frame[column] = pd.Series([None] * len(frame), dtype="object")
        return frame

    def _normalize_frame(self, df, default_columns):
        frame = self._ensure_dataframe(df, default_columns)

        if "item_name" in frame.columns:
            frame["item_name"] = (
                frame["item_name"]
                .astype(str)
                .str.strip()
                .str.upper()
            )

        if "qty" in frame.columns:
            frame["qty"] = pd.to_numeric(frame["qty"], errors="coerce").fillna(0)

        if "quantity" in frame.columns:
            frame.rename(columns={"quantity": "qty"}, inplace=True)
            frame["qty"] = pd.to_numeric(frame["qty"], errors="coerce").fillna(0)

        if "date" in frame.columns:
            frame["date"] = pd.to_datetime(frame["date"], errors="coerce")

        if "time" in frame.columns:
            frame["time"] = frame["time"].astype(str).str.strip()
        else:
            frame["time"] = ""

        if "voucher_no" in frame.columns:
            frame.rename(columns={"voucher_no": "voucher_number"}, inplace=True)
        elif "voucher" in frame.columns:
            frame.rename(columns={"voucher": "voucher_number"}, inplace=True)

        if "voucher_number" in frame.columns:
            frame["voucher_number"] = frame["voucher_number"].fillna("").astype(str).str.strip()
        else:
            frame["voucher_number"] = ""

        if "transaction_sequence" in frame.columns:
            frame["transaction_sequence"] = pd.to_numeric(frame["transaction_sequence"], errors="coerce").fillna(0)
        elif "seq" in frame.columns:
            frame.rename(columns={"seq": "transaction_sequence"}, inplace=True)
            frame["transaction_sequence"] = pd.to_numeric(frame["transaction_sequence"], errors="coerce").fillna(0)
        else:
            frame["transaction_sequence"] = 0

        return frame

    def prepare(self):
        self.opening = self._normalize_frame(self.opening, ["item_name", "qty", "mrp", "epr"])
        self.purchase = self._normalize_frame(self.purchase, ["date", "item_name", "qty"])
        self.sales = self._normalize_frame(self.sales, ["date", "item_name", "qty"])
        self.adjustment = self._normalize_frame(self.adjustment, ["date", "item_name", "qty"])
        self.stock_modify = self._normalize_frame(self.stock_modify, ["date", "item_name", "qty"])
        self.purchase_return = self._normalize_frame(self.purchase_return, ["date", "item_name", "qty"])
        self.sales_return = self._normalize_frame(self.sales_return, ["date", "item_name", "qty"])
        self.transfer = self._normalize_frame(self.transfer, ["date", "item_name", "qty"])

        self.opening_balances = {
            row.item_name: row.qty
            for row in self.opening[["item_name", "qty"]].itertuples(index=False)
        }

        return self

    def _append_transactions(self, frame, transaction_type, sign_mode="positive"):
        transactions = []

        for row in frame.itertuples(index=False):
            qty = float(getattr(row, "qty", 0) or 0)

            if transaction_type == "Sales":
                signed_qty = -abs(qty)
            elif transaction_type == "Purchase":
                signed_qty = abs(qty)
            elif transaction_type in {"Purchase Return", "Sales Return", "Transfer"}:
                signed_qty = qty
            else:
                signed_qty = qty

            transactions.append({
                "date": getattr(row, "date", None),
                "time": getattr(row, "time", ""),
                "voucher_number": getattr(row, "voucher_number", ""),
                "transaction_sequence": getattr(row, "transaction_sequence", 0),
                "item_name": getattr(row, "item_name", ""),
                "transaction_type": transaction_type,
                "qty": qty,
                "signed_qty": signed_qty,
            })

        return transactions

    def build_transactions(self):
        self.prepare()

        transactions = []

        for row in self.opening[["item_name", "qty"]].itertuples(index=False):
            transactions.append({
                "date": None,
                "time": "",
                "voucher_number": "",
                "transaction_sequence": 0,
                "item_name": row.item_name,
                "transaction_type": "Opening Stock",
                "qty": float(row.qty or 0),
                "signed_qty": float(row.qty or 0),
            })

        transactions.extend(self._append_transactions(self.purchase, "Purchase"))
        transactions.extend(self._append_transactions(self.sales, "Sales"))
        transactions.extend(self._append_transactions(self.adjustment, "Stock Adjustment"))
        transactions.extend(self._append_transactions(self.stock_modify, "Stock Modify"))
        transactions.extend(self._append_transactions(self.purchase_return, "Purchase Return"))
        transactions.extend(self._append_transactions(self.sales_return, "Sales Return"))
        transactions.extend(self._append_transactions(self.transfer, "Transfer"))

        transaction_df = pd.DataFrame(transactions)

        if transaction_df.empty:
            transaction_df = pd.DataFrame(columns=[
                "date",
                "time",
                "voucher_number",
                "transaction_sequence",
                "item_name",
                "transaction_type",
                "qty",
                "signed_qty",
            ])

        if not transaction_df.empty:
            transaction_df["date"] = pd.to_datetime(transaction_df["date"], errors="coerce")
            transaction_df["time"] = transaction_df["time"].fillna("").astype(str).str.strip()
            transaction_df["voucher_number"] = transaction_df["voucher_number"].fillna("").astype(str).str.strip()
            transaction_df["transaction_sequence"] = pd.to_numeric(transaction_df["transaction_sequence"], errors="coerce").fillna(0)
            transaction_df["item_name"] = transaction_df["item_name"].astype(str).str.strip().str.upper()
            transaction_df["signed_qty"] = pd.to_numeric(transaction_df["signed_qty"], errors="coerce").fillna(0)
            transaction_df["qty"] = pd.to_numeric(transaction_df["qty"], errors="coerce").fillna(0)
            transaction_df["sort_date"] = transaction_df["date"].fillna(pd.Timestamp("1900-01-01"))
            transaction_df = transaction_df.sort_values(
                ["sort_date", "time", "voucher_number", "transaction_sequence", "item_name"],
                kind="mergesort"
            ).reset_index(drop=True)
            transaction_df.drop(columns=["sort_date"], inplace=True)

        self.transaction_df = transaction_df
        return transaction_df

    def calculate_running_balances(self):
        transaction_df = self.build_transactions()

        if transaction_df.empty:
            self.transaction_df = transaction_df
            return transaction_df

        balances = {}
        running_stock = []

        for row in transaction_df.itertuples(index=False):
            item_name = getattr(row, "item_name", "")
            if not item_name:
                running_stock.append(0)
                continue

            if item_name not in balances:
                balances[item_name] = self.opening_balances.get(item_name, 0)

            if getattr(row, "transaction_type", "") == "Opening Stock":
                balances[item_name] = float(getattr(row, "qty", 0) or 0)
            else:
                balances[item_name] += float(getattr(row, "signed_qty", 0) or 0)

            running_stock.append(balances[item_name])

        transaction_df["running_stock"] = running_stock
        transaction_df.rename(columns={"transaction_type": "Transaction Type"}, inplace=True)
        transaction_df.rename(columns={"running_stock": "Running Stock"}, inplace=True)
        self.transaction_df = transaction_df
        return transaction_df


class StockEngine:

    def __init__(
        self,
        opening_df,
        purchase_df,
        sales_df,
        adjustment_df,
        mode="existing",
        stock_modify_df=None,
        purchase_return_df=None,
        sales_return_df=None,
        transfer_df=None,
    ):

        self.opening = opening_df.copy() if opening_df is not None else pd.DataFrame(columns=["item_name", "qty"])
        self.purchase = purchase_df.copy() if purchase_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.sales = sales_df.copy() if sales_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.adjustment = adjustment_df.copy() if adjustment_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.stock_modify = stock_modify_df.copy() if stock_modify_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.purchase_return = purchase_return_df.copy() if purchase_return_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.sales_return = sales_return_df.copy() if sales_return_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])
        self.transfer = transfer_df.copy() if transfer_df is not None else pd.DataFrame(columns=["date", "item_name", "qty"])

        self.mode = mode

        # Cache for generated reports
        self._daily_stock = None
        self._weekly_stock = None
        self._monthly_stock = None
        self._ledger = None
        self._transaction_engine = None

    # --------------------------------------------------------
    # Standardize Data
    # --------------------------------------------------------
    def prepare(self):
        self._transaction_engine = TransactionEngine(
            self.opening,
            self.purchase,
            self.sales,
            self.adjustment,
            self.stock_modify,
            self.purchase_return,
            self.sales_return,
            self.transfer,
        )
        self._transaction_engine.prepare()
        self.opening = self._transaction_engine.opening
        self.purchase = self._transaction_engine.purchase
        self.sales = self._transaction_engine.sales
        self.adjustment = self._transaction_engine.adjustment
        self.stock_modify = self._transaction_engine.stock_modify
        self.purchase_return = self._transaction_engine.purchase_return
        self.sales_return = self._transaction_engine.sales_return
        self.transfer = self._transaction_engine.transfer
        self._ledger = self._transaction_engine.calculate_running_balances()
        self._opening_stock = self._transaction_engine.opening_balances

    # --------------------------------------------------------
    # Daily Stock Report
    # --------------------------------------------------------
    def daily_stock(self):

        if self._daily_stock is not None:
            return self._daily_stock

        self.prepare()

        transaction_df = self._ledger.copy()
        if transaction_df.empty:
            df = pd.DataFrame(columns=[
                "Date",
                "Item Name",
                "Opening Qty",
                "Purchase Qty",
                "Sales Qty",
                "Adjustment Qty",
                "Stock Modify Qty",
                "Closing Qty",
                "MRP",
                "EPR",
                "MRP Value",
                "EPR Value",
            ])
            self._daily_stock = df
            logging.info("Daily Stock Report Generated")
            return self._daily_stock

        valid_dates = transaction_df["date"].dropna().sort_values()
        if valid_dates.empty:
            self._daily_stock = pd.DataFrame(columns=[
                "Date",
                "Item Name",
                "Opening Qty",
                "Purchase Qty",
                "Sales Qty",
                "Adjustment Qty",
                "Stock Modify Qty",
                "Closing Qty",
                "MRP",
                "EPR",
                "MRP Value",
                "EPR Value",
            ])
            logging.info("Daily Stock Report Generated")
            return self._daily_stock

        start_date = valid_dates.min().normalize()
        end_date = valid_dates.max().normalize()

        opening_stock = dict(self._opening_stock)

        mrp_dict = {}
        epr_dict = {}

        if "mrp" in self.opening.columns:
            for row in self.opening[["item_name", "mrp"]].itertuples(index=False):
                mrp_dict[row.item_name] = float(row.mrp or 0)
        else:
            mrp_dict = {item: 0 for item in self.opening["item_name"].tolist()}

        if "epr" in self.opening.columns:
            for row in self.opening[["item_name", "epr"]].itertuples(index=False):
                epr_dict[row.item_name] = float(row.epr or 0)
        else:
            epr_dict = {item: 0 for item in self.opening["item_name"].tolist()}

        report = []
        previous_closing = dict(opening_stock)

        dates = pd.date_range(start_date, end_date, freq="D")

        for current_date in dates:
            is_first_day = current_date == start_date

            day_transactions = transaction_df[
                transaction_df["date"].dt.normalize() == current_date
            ]

            items = set(opening_stock.keys())
            items.update(day_transactions["item_name"].tolist())

            for item in sorted(items):
                opening_qty = previous_closing.get(item, opening_stock.get(item, 0))

                if self.mode == "golive" and is_first_day:
                    opening_qty = 0

                item_transactions = day_transactions[day_transactions["item_name"] == item]

                transaction_column = "Transaction Type"
                if transaction_column not in item_transactions.columns:
                    transaction_column = "transaction_type"

                purchase_qty = item_transactions.loc[
                    item_transactions[transaction_column] == "Purchase",
                    "signed_qty",
                ].sum()
                sales_qty = -item_transactions.loc[
                    item_transactions[transaction_column] == "Sales",
                    "signed_qty",
                ].sum()
                adjustment_qty = item_transactions.loc[
                    item_transactions[transaction_column] == "Stock Adjustment",
                    "signed_qty",
                ].sum()
                stock_modify_qty = item_transactions.loc[
                    item_transactions[transaction_column] == "Stock Modify",
                    "signed_qty",
                ].sum()
                delta_total = item_transactions["signed_qty"].sum()
                closing_qty = opening_qty + delta_total

                report.append({
                    "Date": current_date.date(),
                    "Item Name": item,
                    "Opening Qty": opening_qty,
                    "Purchase Qty": purchase_qty,
                    "Sales Qty": sales_qty,
                    "Adjustment Qty": adjustment_qty,
                    "Stock Modify Qty": stock_modify_qty,
                    "Closing Qty": closing_qty,
                    "MRP": mrp_dict.get(item, 0),
                    "EPR": epr_dict.get(item, 0),
                    "MRP Value": closing_qty * mrp_dict.get(item, 0),
                    "EPR Value": closing_qty * epr_dict.get(item, 0),
                })

                previous_closing[item] = closing_qty

        df = pd.DataFrame(report)
        self._daily_stock = df
        logging.info("Daily Stock Report Generated")
        return self._daily_stock

    # --------------------------------------------------------
    # Weekly Report
    # --------------------------------------------------------
    def weekly_stock(self):
        if self._weekly_stock is not None:
            return self._weekly_stock

        daily = self.daily_stock()
        if daily.empty:
            self._weekly_stock = daily.copy()
            return self._weekly_stock

        daily["Date"] = pd.to_datetime(daily["Date"])
        daily["Week"] = daily["Date"].dt.strftime("%Y-W%U")

        weekly = (
            daily.groupby(["Week", "Item Name"], as_index=False)
            .agg({
                "Opening Qty": "first",
                "Purchase Qty": "sum",
                "Sales Qty": "sum",
                "Adjustment Qty": "sum",
                "Stock Modify Qty": "sum",
                "Closing Qty": "last",
                "MRP Value": "last",
                "EPR Value": "last",
            })
        )

        self._weekly_stock = weekly
        logging.info("Weekly Stock Report Generated")
        return self._weekly_stock

    # --------------------------------------------------------
    # Monthly Report
    # --------------------------------------------------------
    def monthly_stock(self):
        if self._monthly_stock is not None:
            return self._monthly_stock

        daily = self.daily_stock()
        if daily.empty:
            self._monthly_stock = daily.copy()
            return self._monthly_stock

        daily["Date"] = pd.to_datetime(daily["Date"])
        daily["Month"] = daily["Date"].dt.to_period("M").astype(str)

        monthly = (
            daily.groupby(["Month", "Item Name"], as_index=False)
            .agg({
                "Opening Qty": "first",
                "Purchase Qty": "sum",
                "Sales Qty": "sum",
                "Adjustment Qty": "sum",
                "Stock Modify Qty": "sum",
                "Closing Qty": "last",
                "MRP Value": "last",
                "EPR Value": "last",
            })
        )

        self._monthly_stock = monthly
        logging.info("Monthly Stock Report Generated")
        return self._monthly_stock

    # --------------------------------------------------------
    # Item Ledger
    # --------------------------------------------------------
    def item_ledger(self):
        if self._ledger is not None:
            return self._ledger.copy()
        self.prepare()
        return self._ledger.copy()

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
            self.sales.groupby("item_name")["date"].max().reset_index()
        )

        last_sale["Days"] = (latest - last_sale["date"]).dt.days

        return last_sale[last_sale["Days"] >= days]

    # --------------------------------------------------------
    # Stock Summary
    # --------------------------------------------------------
    def summary(self):
        daily = self.daily_stock()

        return {
            "Total Items": daily["Item Name"].nunique(),
            "Total Closing Qty": daily["Closing Qty"].sum(),
            "Total MRP Value": daily["MRP Value"].sum(),
            "Total EPR Value": daily["EPR Value"].sum(),
        }