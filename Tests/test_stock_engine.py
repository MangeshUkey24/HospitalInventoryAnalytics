from excel_reader import ExcelReader
from stock_engine import StockEngine

print("Reading Excel Files...")

reader = ExcelReader()

data = reader.read_all(
    opening_file=r"D:\YOUR_PATH\Opening.xlsx",
    purchase_file=r"D:\YOUR_PATH\Purchase.xlsx",
    sales_file=r"D:\YOUR_PATH\Sales.xlsx",
    adjustment_file=r"D:\YOUR_PATH\Adjustment.xlsx"
)

print("Excel Read Successfully")

engine = StockEngine(
    data["opening"],
    data["purchase"],
    data["sales"],
    data["adjustment"]
)

print("Calculating Daily Stock...")

result = engine.daily_stock()

print(result.head())

print()

print(engine.summary())