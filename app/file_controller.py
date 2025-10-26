import numpy as np
import pandas as pd


class FileController:
    def __init__(self, csv_file_path: str) -> None:
        self.csv_file_path = csv_file_path

    def remove_empty_rows(self) -> bool:
        try:
            df = pd.read_csv(self.csv_file_path)

            # Replace empty strings or strings with only whitespace with NaN
            # and drop rows with all NaN values
            df_cleaned = df.replace(r"^\s*$", np.nan, regex=True).dropna(how="all")

            # Save the cleaned DataFrame back to the CSV file
            df_cleaned.to_csv(self.csv_file_path, index=False)
            return True
        except Exception as e:
            print(f"An error occurred while removing empty rows: {e}")
            return False
