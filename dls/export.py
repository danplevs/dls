from pathlib import Path
import pandas as pd


def export(data: pd.DataFrame, path: Path, mode="w"):
    data.to_csv(path, header=None, index=None, sep=" ", mode=mode)
