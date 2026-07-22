from excel_reader import ExcelReader
from stock_engine import StockEngine

# -------------------------------
# Enter your Excel file paths
# -------------------------------

OPENING_FILE = r"D:\MEGA Oakland\MEDNET 26-27 Clients\Achyut Maharaj Hospital\OPD Pharmacy\Opening Stock Report.xlsx"

PURCHASE_FILE = r"D:\MEGA Oakland\MEDNET 26-27 Clients\Achyut Maharaj Hospital\OPD Pharmacy\Purchase Report.xlsx"

SALES_FILE = r"D:\MEGA Oakland\MEDNET 26-27 Clients\Achyut Maharaj Hospital\OPD Pharmacy\Patient Wise Sales Report.xlsx"

ADJUSTMENT_FILE = r"D:\MEGA Oakland\MEDNET 26-27 Clients\Achyut Maharaj Hospital\OPD Pharmacy\Stock Adjustment Report.xlsx"

print("=" * 60)
print("HIAS STOCK ENGINE TEST")
print("=" * 60)

try:
    print("\nReading Excel Files...")

    reader = ExcelReader()

    data = reader.read_all(
        opening_file=OPENING_FILE,
        purchase_file=PURCHASE_FILE,
        sales_file=SALES_FILE,
        adjustment_file=ADJUSTMENT_FILE
    )

    print("SUCCESS : Excel files loaded")

    print(f"Opening Rows   : {len(data['opening'])}")
    print(f"Purchase Rows  : {len(data['purchase'])}")
    print(f"Sales Rows     : {len(data['sales'])}")
    print(f"Adjustment Rows: {len(data['adjustment'])}")

    print("\nCreating Stock Engine...")

    engine = StockEngine(
        data["opening"],
        data["purchase"],
        data["sales"],
        data["adjustment"]
    )

    print("SUCCESS : Stock Engine Created")

    print("\nGenerating Daily Stock Report...")

    report = engine.daily_stock()

    print("SUCCESS : Report Generated")

    print("\nFirst 10 Records")
    print(report.head(10))

    print("\nSummary")
    print(engine.summary())

    print("\nTEST COMPLETED SUCCESSFULLY")

except Exception as e:
    print("\nERROR OCCURRED")
    print(type(e).__name__)
    print(e)