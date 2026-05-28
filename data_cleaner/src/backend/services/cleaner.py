import pandas as pd
import os
from typing import Any


class SheetCleaner:
    def __init__(self, file_name: str, file_path: str):
        self.file_name = file_name
        self.file_path = file_path  # router provides the real path
        self.data = None
        self.file_storage = None  # set after detecting file type

        # Resolve backend root
        self.services_dir = os.path.dirname(os.path.abspath(__file__))
        self.backend_dir = os.path.dirname(self.services_dir)

    # ---------------------------------------------------------
    # LOAD (CSV + Excel)
    # ---------------------------------------------------------
    def load_data(self):
        """Load CSV or Excel file into a DataFrame."""
        try:
            ext = os.path.splitext(self.file_name)[1].lower()

            if ext == ".csv":
                self.data = pd.read_csv(self.file_path)
                self.file_storage = "save_csv"

            elif ext in [".xlsx", ".xls"]:
                self.data = pd.read_excel(self.file_path)
                self.file_storage = "save_excel"

            else:
                raise ValueError(f"Unsupported file type: {ext}")

            self.normalize_columns()

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {e}")

    # ---------------------------------------------------------
    # CLEANING STEPS
    # ---------------------------------------------------------
    def normalize_columns(self):
        self.data.columns = (
            self.data.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(r"[^a-zA-Z0-9_]", "", regex=True)
        )

    def handle_missing(
        self,
        strategy: str,
        columns: list | None = None,
        fill_value=None
    ):
        """
        Handle missing values in the dataset.

        Parameters
        ----------
        strategy : str
        Strategy to use:
            - drop
            - mean
            - median
            - mode
            - constant
            - ffill
            - bfill

        columns : list | None
            Specific columns to apply strategy to. If None, all columns are used.

        fill_value :
            Value used for constant strategy.
        """

        df = self.data

        # Use all columns if none specified
        if columns is None:
            columns = df.columns

        # Validate columns
        invalid_cols = [col for col in columns if col not in df.columns]
        if invalid_cols:
            raise ValueError(f"Invalid columns: {invalid_cols}")

        # DROP ROWS WITH MISSING VALUES
        if strategy == "drop":
            df = df.dropna(subset=columns)

        # MEAN IMPUTATION
        elif strategy == "mean":
            for col in columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())

        # MEDIAN IMPUTATION
        elif strategy == "median":
            for col in columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())

        # MODE IMPUTATION
        elif strategy == "mode":
            for col in columns:
                mode_value = df[col].mode()
                if not mode_value.empty:
                    df[col] = df[col].fillna(mode_value[0])

        # CONSTANT VALUE IMPUTATION
        elif strategy == "constant":
            if fill_value is None:
                raise ValueError("fill_value must be provided for constant strategy")
            df[columns] = df[columns].fillna(fill_value)

        # FORWARD FILL
        elif strategy == "ffill":
            df[columns] = df[columns].fillna(method="ffill")

        # BACKWARD FILL
        elif strategy == "bfill":
            df[columns] = df[columns].fillna(method="bfill")

        else:
            raise ValueError(f"Unsupported strategy: {strategy}")

        self.data = df
        return self.data


    def remove_duplicates(self):
        self.data = self.data.drop_duplicates()

    # ---------------------------------------------------------
    # STATS
    # ---------------------------------------------------------
    def generate_stats(self):
        return {
            "shape": self.data.shape,
            "columns": list(self.data.columns),
            "missing": self.data.isna().sum().to_dict(),
            "describe": self.data.describe(include="all").to_dict()
        }

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    def save_cleaned_data(self):
        """Save cleaned data as CSV (Excel → CSV conversion)."""

        # Determine save directory based on file type
        save_dir = os.path.join(self.backend_dir, "models", self.file_storage)
        os.makedirs(save_dir, exist_ok=True)

        # Always save as CSV
        output_name = (
            self.file_name
            .replace(".xlsx", ".csv")
            .replace(".xls", ".csv")
        )
        output_path = os.path.join(save_dir, output_name)

        if self.data is None:
            raise ValueError("No cleaned data to save. Run the pipeline first.")

        try:
            self.data.to_csv(output_path, index=False)
            return output_path
        except Exception as e:
            raise Exception(f"Error saving cleaned data: {e}")

    # ---------------------------------------------------------
    # FULL PIPELINE
    # ---------------------------------------------------------
    def run(self, fill_value : Any, columns: list, missing_strategy: str):
        self.load_data()
        self.handle_missing(strategy=missing_strategy,
                            columns=columns,
                            fill_value=fill_value)
        self.remove_duplicates()
        return self.generate_stats()
