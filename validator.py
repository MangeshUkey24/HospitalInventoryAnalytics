"""
------------------------------------------------------------
Hospital Inventory Analytics System (HIAS)
Data Validator
------------------------------------------------------------
"""

class DataValidator:

    @staticmethod
    def validate_columns(df, required_columns, report_name):
        """
        Validate required columns in a DataFrame.
        """

        missing = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"{report_name}\n\n"
                f"Missing required column(s): "
                f"{', '.join(missing)}"
            )

    @staticmethod
    def validate_empty(df, report_name):

        if df.empty:
            raise ValueError(
                f"{report_name} contains no data."
            )