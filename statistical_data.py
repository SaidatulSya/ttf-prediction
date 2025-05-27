import pandas as pd

class StatisticalData:
    def __init__(self, df: pd.DataFrame):
        if df is None or df.empty:
            raise ValueError ("Provided DataFrame is empty or None.")
        if "value" not in df.columns:
            raise ValueError ("Expected a column named 'value' in the DataFrame")
        self.df = df

    def median(self):
        return self.df["value"].median()

    def mean_absolute_dev(self):
        return self.df["value"].mad()

    def standard_dev(self):
        return self.df["value"].mad()

    def mean(self):
        return self.df["value"].mean()

    def rolling_median(self, window: int = 3, start: str = None, end: str = None):
        df = self.df.copy()

        if start:
            df = df[df.index >= pd.to_datetime(start)]

        if end:
            df = df[df.index <= pd.to_datetime(end)]

        rolling_result = df["value"].rolling(window=window).median()
        return rolling_result