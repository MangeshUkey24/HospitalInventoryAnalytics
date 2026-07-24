import pandas as pd


class MasterDataAuditEngine:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_file(self):
        try:
            self.df = pd.read_excel(self.file_path)

            print("File Loaded Successfully")
            print(f"Total Records : {len(self.df)}")

            return True

        except Exception as e:
            print(f"Error : {e}")
            return False

    def get_columns(self):
        if self.df is None:
            return []

        return self.df.columns.tolist()

    def total_records(self):
        if self.df is None:
            return 0

        return len(self.df)