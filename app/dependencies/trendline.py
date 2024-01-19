from scipy.stats import linregress
import numpy as np


def calculate_trendline(df):
    df_high = df.iloc[:-5]
    df_low = df.iloc[:-5]

    trendline_vars = {"upper": {}, "lower": {}}

    # get points for upper trendline
    while len(df_high) > 10:
        slope, intercept, r_value, p_value, std_er = linregress(
            x=df_high["number"], y=df_high["high"]
        )
        df_high = df_high.loc[
            df_high["high"] > slope * df_high["number"] + intercept
        ]

    # get points for lower trendline
    while len(df_low) > 10:
        slope, intercept, r_value, p_value, std_er = linregress(
            x=df_low["number"], y=df_low["low"]
        )
        df_low = df_low.loc[
            df_low["low"] < slope * df_low["number"] + intercept
        ]

    return {"upper": df_high, "lower": df_low}
