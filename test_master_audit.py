from audit.master_data.audit_engine import MasterDataAuditEngine

# Excel File Path
file_path = r"Input\ItemMasterCopy.xlsx"

# Create Engine
engine = MasterDataAuditEngine(file_path)

# Load Excel
if engine.load_file():

    print("\nAudit Ready")

    print("\nColumns:")

    print(engine.get_columns())

    print("\nTotal Records:")

    print(engine.total_records())
    import pandas as pd

file_path = r"Input\ItemMasterCopy.xlsx"

df = pd.read_excel(file_path, header=None)

print(df.head(15))