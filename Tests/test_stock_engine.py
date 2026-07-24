import pandas as pd

from stock_engine import StockEngine


def test_stock_modify_transactions_affect_running_balance():
    opening = pd.DataFrame([
        {"item_name": "ABC", "qty": 0}
    ])

    purchase = pd.DataFrame(columns=["date", "item_name", "qty"])

    sales = pd.DataFrame([
        {"date": "2024-01-01", "item_name": "ABC", "qty": 30}
    ])

    adjustment = pd.DataFrame([
        {"date": "2024-01-01", "item_name": "ABC", "qty": 117}
    ])

    stock_modify = pd.DataFrame([
        {"date": "2024-01-01", "item_name": "ABC", "qty": -87},
        {"date": "2024-01-01", "item_name": "ABC", "qty": 87},
    ])

    engine = StockEngine(
        opening,
        purchase,
        sales,
        adjustment,
        stock_modify_df=stock_modify,
    )

    daily = engine.daily_stock()
    ledger = engine.item_ledger()

    assert daily.loc[daily["Item Name"] == "ABC", "Closing Qty"].iloc[0] == 87

    stock_modify_rows = ledger[ledger["Transaction Type"] == "Stock Modify"]
    assert not stock_modify_rows.empty
    assert stock_modify_rows["Running Stock"].iloc[-1] == 87
