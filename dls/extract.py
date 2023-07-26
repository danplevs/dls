from pathlib import Path
from typing import Dict, List

import pandas as pd

def read_replicates(data_file: Path) -> Dict[int, pd.DataFrame]:
    xl = pd.ExcelFile(data_file)
    second_to_last_sheets = xl.sheet_names[1:]
    return {index: xl.parse(sheet) for index, sheet in enumerate(second_to_last_sheets, start=1)}


def extract_size_by_intensity(data: pd.DataFrame) -> pd.DataFrame:
    return data.iloc[7:, [5, 6]].dropna(how="all")


def extract_correlation_fn(data: pd.DataFrame) -> pd.DataFrame:
    return data.iloc[7:, [13, 14, 15]].dropna(how="all")


def extract_size_results(data: pd.DataFrame) -> pd.DataFrame:
    return data.iloc[[5, 6, 9, 10, 22, 24], [1, 2, 3]]


def extract_zeta_distribution(data: pd.DataFrame) -> pd.DataFrame:
    return data.iloc[7:, [5, 6]]


def extract_phase_plot(data: pd.DataFrame) -> pd.DataFrame:
    return data.iloc[7:, [8, 9, 10, 11]]


def extract_zeta_results(data: pd.DataFrame) -> pd.DataFrame:
    return data.iloc[[5, 6], [1, 2]]
