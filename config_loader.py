"""
------------------------------------------------------------
Hospital Inventory Analytics System (HIAS)
Configuration Loader
------------------------------------------------------------
Author : Mangesh Ukey
Version : 1.0
------------------------------------------------------------
"""

import json
import os


class ConfigLoader:
    def __init__(self, config_path="Config/hospital_config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def standardize_columns(self, df):
        """
        Rename DataFrame columns using hospital_config.json mappings.
        """

        mapping = self.config.get("column_mapping", {})

        rename_dict = {}

        for standard_name, aliases in mapping.items():
            for alias in aliases:
                for column in df.columns:
                    if str(column).strip().lower() == str(alias).strip().lower():
                        rename_dict[column] = standard_name

        df = df.rename(columns=rename_dict)

        return df