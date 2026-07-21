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
import logging


class ConfigLoader:

    def __init__(self,
                 config_file="Config/hospital_config.json"):

        self.config_file = config_file

        self.config = {}

        self.load()

    # --------------------------------------------------------
    # Load JSON Configuration
    # --------------------------------------------------------
    def load(self):

        try:

            if not os.path.exists(self.config_file):

                raise FileNotFoundError(
                    f"Configuration file not found : {self.config_file}"
                )

            with open(
                self.config_file,
                "r",
                encoding="utf-8"
            ) as file:

                self.config = json.load(file)

            logging.info("Configuration Loaded Successfully")

        except Exception as e:

            logging.exception(e)

            raise

    # --------------------------------------------------------
    # Get Complete Configuration
    # --------------------------------------------------------
    def get_config(self):

        return self.config

    # --------------------------------------------------------
    # Get Section
    # --------------------------------------------------------
    def get(self, key, default=None):

        return self.config.get(key, default)

    # --------------------------------------------------------
    # Get Column Mapping
    # --------------------------------------------------------
    def get_column_mapping(self):

        return self.config.get("column_mapping", {})

    # --------------------------------------------------------
    # Get Report Settings
    # --------------------------------------------------------
    def get_reports(self):

        return self.config.get("reports", {})

    # --------------------------------------------------------
    # Find Standard Column Name
    # --------------------------------------------------------
    def identify_column(self, actual_column):

        actual_column = actual_column.strip().lower()

        mappings = self.get_column_mapping()

        for standard_name, aliases in mappings.items():

            for alias in aliases:

                if actual_column == alias.lower():

                    return standard_name

        return None

    # --------------------------------------------------------
    # Convert All Columns
    # --------------------------------------------------------
    def standardize_columns(self, dataframe):

        rename_dict = {}

        for column in dataframe.columns:

            standard = self.identify_column(column)

            if standard:

                rename_dict[column] = standard

        dataframe = dataframe.rename(columns=rename_dict)

        return dataframe

    # --------------------------------------------------------
    # Print Configuration
    # --------------------------------------------------------
    def print_config(self):

        print(json.dumps(self.config, indent=4))