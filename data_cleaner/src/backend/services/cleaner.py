import pandas as pd
import numpy as np
import os
from typing import Any, Dict, List


class SheetCleaner:
    def __init__(self, file_name: str, file_path: str):
        self.file_name = file_name
        self.file_path = file_path
        self.data: pd.DataFrame | None = None

        # Resolve backend root
        self.services_dir = os.path.dirname(os.path.abspath(__file__))
        self.backend_dir = os.path.dirname(self.services_dir)

        # Will be set after load
        self.file_storage = None

    # ---------------------------------------------------------
    # LOAD
    # ---------------------------------------------------------
    def load_data(self):
        ext = os.path.splitext(self.file_name)[1].lower()

        if ext == ".csv":
            df = pd.read_csv(self.file_path)
            self.file_storage = "save_csv"

        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(self.file_path)
            self.file_storage = "save_excel"

        else:
            raise ValueError(f"Unsupported file type: {ext}")

        # Normalize columns
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(r"[^a-zA-Z0-9_]", "", regex=True)
        )

        self.data = df

    # ---------------------------------------------------------
    # MISSING VALUE HANDLING
    # ---------------------------------------------------------
    def handle_missing(
        self,
        strategy: str,
        columns: List[str] | None = None,
        fill_value: Any = None
    ):
        if self.data is None:
            raise ValueError("Data not loaded")

        df = self.data

        # Default to all columns
        if columns is None:
            columns = df.columns.tolist()

        # Remove empty column names (common UI bug)
        columns = [c for c in columns if c and c.strip()]

        if not columns:
            raise ValueError("No valid columns provided")

        # Validate columns
        invalid = [c for c in columns if c not in df.columns]
        if invalid:
            raise ValueError(f"Invalid columns: {invalid}. Valid columns: {df.columns.tolist()}")

        # STRATEGY: DROP
        if strategy == "drop":
            try:
                df = df.dropna(subset=columns)
            except Exception as e:
                raise ValueError(f"Error applying DROP strategy: {e}")

        # STRATEGY: MEAN
        elif strategy == "mean":
            try:
                for col in columns:
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        raise ValueError(f"Column '{col}' is not numeric, cannot apply MEAN")
                    df[col] = df[col].fillna(df[col].mean())
            except Exception as e:
                raise ValueError(f"Error applying MEAN strategy: {e}")

        # STRATEGY: MEDIAN
        elif strategy == "median":
            try:
                for col in columns:
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        raise ValueError(f"Column '{col}' is not numeric, cannot apply MEDIAN")
                    df[col] = df[col].fillna(df[col].median())
            except Exception as e:
                raise ValueError(f"Error applying MEDIAN strategy: {e}")

        # STRATEGY: MODE
        elif strategy == "mode":
            try:
                for col in columns:
                    mode_val = df[col].mode()
                    if mode_val.empty:
                        raise ValueError(f"Column '{col}' has no mode value")
                    df[col] = df[col].fillna(mode_val[0])
            except Exception as e:
                raise ValueError(f"Error applying MODE strategy: {e}")

        # STRATEGY: CONSTANT
        elif strategy == "constant":
            try:
                if fill_value is None:
                    raise ValueError("fill_value must be provided for CONSTANT strategy")
                df[columns] = df[columns].fillna(fill_value)
            except Exception as e:
                raise ValueError(f"Error applying CONSTANT strategy: {e}")

        # STRATEGY: FORWARD FILL — use .ffill() directly (fillna(method=) removed in pandas 2.2+)
        elif strategy == "ffill":
            try:
                df[columns] = df[columns].ffill()
            except Exception as e:
                raise ValueError(f"Error applying FORWARD FILL (ffill): {e}")

        # STRATEGY: BACKWARD FILL — use .bfill() directly (fillna(method=) removed in pandas 2.2+)
        elif strategy == "bfill":
            try:
                df[columns] = df[columns].bfill()
            except Exception as e:
                raise ValueError(f"Error applying BACKWARD FILL (bfill): {e}")

        else:
            raise ValueError(f"Unsupported strategy: {strategy}")

        self.data = df

    # ---------------------------------------------------------
    # DUPLICATES
    # ---------------------------------------------------------
    def remove_duplicates(self):
        if self.data is None:
            raise ValueError("Data not loaded")
        self.data = self.data.drop_duplicates()

    # ---------------------------------------------------------
    # STATS (JSON SAFE)
    # ---------------------------------------------------------
    def generate_stats(
        self,
        strategy: str,
        missing_before: Dict[str, int],
        missing_after: Dict[str, int],
        rows_before: int,
        rows_after: int,
        fill_value: Any
    ):
        return {
            "strategy": strategy,
            "missing_before": missing_before,
            "missing_after": missing_after,
            "rows_before": rows_before,
            "rows_after": rows_after,
            "fill_value": fill_value,
        }

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    def save_cleaned_data(self):
        if self.data is None:
            raise ValueError("No cleaned data to save")

        save_dir = os.path.join(self.backend_dir, "models", self.file_storage)
        os.makedirs(save_dir, exist_ok=True)

        output_name = (
            self.file_name
            .replace(".xlsx", ".csv")
            .replace(".xls", ".csv")
        )
        output_path = os.path.join(save_dir, output_name)

        self.data.to_csv(output_path, index=False)
        return output_path

    # ---------------------------------------------------------
    # FULL PIPELINE
    # ---------------------------------------------------------
    def run(self, fill_value: Any, columns: List[str], missing_strategy: str):
        self.load_data()

        df = self.data
        missing_before = df.isna().sum().to_dict()
        rows_before = len(df)

        # Normalize incoming column names
        columns = [c.lower().strip() for c in columns]

        self.handle_missing(
            strategy=missing_strategy,
            columns=columns,
            fill_value=fill_value
        )

        self.remove_duplicates()

        df = self.data
        missing_after = df.isna().sum().to_dict()
        rows_after = len(df)

        stats = self.generate_stats(
            strategy=missing_strategy,
            missing_before=missing_before,
            missing_after=missing_after,
            rows_before=rows_before,
            rows_after=rows_after,
            fill_value=fill_value
        )

        return stats