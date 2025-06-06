import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class AnalyzeData:
    """ Analyze distribution of data, particularly on missing value
    Note: Ensure your DataFrame has a column named 'Timestamp' before passing it in.
    Useful pandas function:
    df.head() -- to view the first 5 columns
    df.shape() -- to view the row x column of the dataset
    df.info() -- to view total number of non-null 
    """
    def __init__(self, df: pd.DataFrame, filename=None):
        if df is None or df.empty:
            raise ValueError("Provided DataFrame is empty or None.")

        if not pd.api.types.is_datetime64_any_dtype(df.index):
            if "Timestamp" in df.columns:
                df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
                df = df.set_index("Timestamp")
            else:
                raise ValueError("Timestamp column not found. Please ensure the column is named 'Timestamp'")
                    
        self.df = df
        self.filename = filename or "output"
        self.cleaned_df = None
        

    def plot_missing_binary(self):
        """
        Plot a binary timeline of missing vs present data.
        White = data present, Black = missing.
        Only supports single PI tag (one column)
        """

        if self.df["value"].isna().sum() == 0:
            print("No missing data to plot.")
            return

        plt.figure(figsize=(15, 1.5))
        plt.title("Missing Data Timeline (1 = Missing, 0 = Present)")

        mask = self.df["value"].isna().to_frame().T
        plt.imshow(mask, aspect='auto', cmap='gray_r', interpolation='none')

        plt.yticks([0], ["value"])
        plt.xticks([])
        plt.xlabel("Time progression →")
        plt.tight_layout()
        plt.show()

    def interpolate_data(self, method="time"):
        self.cleaned_df = self.df.interpolate(method=method)
        print(f"Interpolated missing values using method: {method}")
        print(f"New total number rows = {len(self.cleaned_df)}")

    def impute_missing(self, method="median"):
        """
        Impute missing values in 'value' column using desired statisctical method. 
        Options:
        'mean' -- fills NaN with the mean of the column
        'median' -- fills NaN with the median of the column
        'mad' fills NaN with the Mean Absolute Deviation
        """
        if self.cleaned_df is None:
            self.cleaned_df = self.df.copy()

        for col in self.cleaned_df.columns:
            if method == "median":
                val = self.cleaned_df[col].median()
            elif method == "mean":
                val = self.cleaned_df[col].mean()
            elif method == "mad":
                val = self.cleaned_df[col].mad()
            else:
                raise ValueError("Invalid imputation method. Choose from 'mean', 'median' or 'mad'")

            self.cleaned_df[col].fillna(val, inplace=True)
            print (f"Filled NaNs in {col} using {method}: {val:.4f}")

        print("Imputation complete")
        return self.cleaned_df

    def outliers_bounds(self,value_col = "value"):
        q1 = np.percentile(self.df[value_col], 25)
        q3 = np.percentile(self.df[value_col], 75)
        iqr = q3-q1

        lb = q1 - 1.5 * iqr
        ub = q3 + 1.5 * iqr

        print('Lower bound:', round(lb,2))
        print('Upper bound:', round(ub,2))
        return lb, ub

    def remove_outliers(self, value_col="value"):
        lb, ub = self.outliers_bounds(value_col)
        original_len = len(self.df)
        self.df = self.df[(self.df[value_col] >= lb) & (self.df[value_col] <= ub)]
        print(f"Removed {original_len - len(self.df)} outliers.")
        

    def box_plot(self, value_col="value"):
        plt.figure(figsize=(10,2))
        self.df.boxplot(column=value_col, vert=False, grid=True)
        plt.title(f"Boxplot of {value_col}")
        plt.grid(True)
        plt.show()
        

    def save_to_csv(self):
        if self.cleaned_df is not None:
            filename = f"{self.filename}_cleaned.csv"
            self.cleaned_df.to_csv(filename)
            print(f"Saved cleaned data to: {filename}")
        else:
            print("No cleaned data available to save.")

        
