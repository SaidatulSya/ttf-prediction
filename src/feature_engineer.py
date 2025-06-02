import pandas as pd
import numpy as np

class FeatureEngineer:

    def __init__(self, df, tag_type='PV', context_df=None):
        self.df = df
        self.context_df = context_df  # Optional context tag like CO or OP

    def assign_status(self, low_alarm, high_alarm, value_col="value"):
        """Improved rule-based anomaly status labeling using multiple features"""
        def classify(row, value_col=value_col, low_alarm=low_alarm, high_alarm=high_alarm):
            val = row[value_col]
            sigma = row["sigma_level"]
            slope = row["slope"]
            r_slope = row["rolling_slope_5"]
            r_std = row["rolling_std_5"]
            r_mad = row["rolling_mad_5"]
            lag_diff = row["lag_diff"]

            if pd.isna(val):
                return "Bad Data"
            elif val < low_alarm:
                return "Low Alarm"
            elif val > high_alarm:
                return "High Alarm"
            elif (
                sigma > 3 or
                (abs(slope) > 3 and abs(lag_diff) > 3) or
                abs(r_slope) > 0.5 or
                r_std > 1 or
                sigma > 2 or
                r_mad > 2
            ):
                return "Anomaly"
            else:
                return "Normal"
        self.df["status"] = self.df.apply(classify, axis=1)
        return self.df

            

    def calculate_ttf(self):
        """Label Time to Failure (TTF) from anomaly to next alarm"""
        self.df["TTF"] = None
        alarm_rows = self.df[self.df["status"].isin(["Low Alarm", "High Alarm"])]
        for i in self.df.index:
            if self.df.at[i, "status"] == "Anomaly":
                current_time = i
                future_alarm = alarm_rows[alarm_rows.index > current_time]
                if not future_alarm.empty:
                    next_alarm_time = future_alarm.index[0]
                    ttf_hours = (next_alarm_time - current_time).total_seconds() / 3600
                    self.df.at[i, "TTF"] = round(ttf_hours, 2)
        return self.df

    def deviation_from_mean(self, value_col="value"):
        """Add deviation and abs deviation from global mean"""
        mean = self.df[value_col].mean()
        self.df["deviation_from_mean"] = self.df[value_col] - mean
        self.df["abs_deviation"] = self.df["deviation_from_mean"].abs()
        return self.df

    def deviation_from_median(self, value_col="value"):
        """Add deviation and absolute deviation from global median"""
        median = self.df[value_col].median()
        self.df["deviation_mad"] = self.df[value_col] - median
        self.df["abs_dev_mad"] = self.df["deviation_mad"].abs()
        return self.df

    def sigma_level(self, value_col="value"):
        """Add how many sigma (std) each value is from mean"""
        std = self.df[value_col].std()
        if "abs_deviation" not in self.df.columns:
            self.deviation_from_mean(value_col)
        self.df["sigma_level"] = self.df["abs_deviation"] / std
        return self.df

    def slope(self, value_col="value"):
        """Add slope = difference between current and previous value"""
        self.df["slope"] = self.df[value_col].diff()
        return self.df

    def rolling_features(self, value_col="value", window=5):
        """Add rolling mean, std, and MAD"""
        self.df[f"rolling_mean_{window}"] = self.df[value_col].rolling(window=window).mean()
        self.df[f"rolling_std_{window}"] = self.df[value_col].rolling(window=window).std()
        self.df[f"rolling_mad_{window}"] = self.df[value_col].rolling(window=window).apply(
            lambda x: np.median(np.abs(x - np.median(x))), raw=True
        )
        return self.df

    def rolling_slope(self, value_col="value", window=5):
        """Add slope of rolling window using manual linear regression"""
        slopes = []
        values = self.df[value_col].values
        x = np.arange(window)

        for i in range(len(self.df)):
            if i < window - 1:
                slopes.append(np.nan)
            else:
                y = values[i - window + 1:i + 1]
                x_mean, y_mean = x.mean(), y.mean()
                numerator = np.sum((x - x_mean) * (y - y_mean))
                denominator = np.sum((x - x_mean) ** 2)
                slope = numerator / denominator if denominator != 0 else 0
                slopes.append(slope)

        self.df[f"rolling_slope_{window}"] = slopes
        return self.df

    def lag_features(self, value_col="value"):
        """Add lag features and lag difference"""
        self.df["lag1"] = self.df[value_col].shift(1)
        self.df["lag_diff"] = self.df[value_col] - self.df["lag1"]
        return self.df

    def generate_all_features(self, value_col="value", window=5):
        """Run all feature engineering steps in sequence"""
        self.deviation_from_mean(value_col)
        self.deviation_from_median(value_col)
        self.sigma_level(value_col)
        self.slope(value_col)
        self.rolling_features(value_col, window)
        self.rolling_slope(value_col, window)
        self.lag_features(value_col)
        return self.df



