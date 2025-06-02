import pandas as pd

class EstTTF:
    def __init__ (self, df, high_alarm, low_alarm, value_col="value", slope_col="rolling_slope_5"):
        self.df = df
        self.high_alarm = high_alarm
        self.low_alarm = low_alarm
        self.value_col = value_col
        self.slope_col = slope_col

    def estimate_ttf(self):
        """
        Estimate TTF based on linear extrapolation using the rolling slope.
        For each row labeled 'Anomaly', estimate when it will hit low/high alarm
        """

        self.df["Est_TTF_Hours"] = None

        for idx, row in self.df.iterrows():
            if row.get("status") != "Anomaly":
                continue

            y0 = row[self.value_col]
            m = row[self.slope_col]

            if pd.isna(m) or m == 0:
                continue #Cannot estimate with zero or NaN slope

            #Determine direction to the nearest alarm (high/low)
            if m > 0:
                y_alarm = self.high_alarm
            else:
                y_alarm = self.low_alarm

            try:
                ttf_sec = (y_alarm - y0) / m
                ttf_hours = ttf_sec /3600

                if ttf_hours > 0:
                    self.df.at[idx, "Est_TTF_Hours"] = round(ttf_hours,2)
            except:
                continue

        return self.df               
