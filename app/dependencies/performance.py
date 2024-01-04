import yfinance as yf
import pandas as pd
from .atr import calculate_atr


async def get_sp_500_change(start: str, end: str):
    sp500 = yf.download(tickers=["SPY"], start=start, end=end)

    sp500.index.names = ["datetime"]
    sp500.columns = sp500.columns.str.lower()

    sp500_change = (
        sp500.iloc[-1]["close"] - sp500.iloc[0]["close"]
    ) / sp500.iloc[0]["close"]

    return sp500_change


async def get_outperformers(start, end, sp500_change):
    constituents = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )[0]

    constituents.index = constituents["Symbol"]
    constituents = constituents[
        ["Security", "GICS Sector", "GICS Sub-Industry"]
    ]
    constituents.index.names = ["symbol"]
    constituents = constituents.rename(
        columns={
            "Security": "name",
            "GICS Sector": "sector",
            "GICS Sub-Industry": "subIndustry",
        }
    )
    constituents.index = constituents.index.str.replace(".", "-")

    df = yf.download(
        tickers=constituents.index.to_list(),
        interval="1d",
        end=end,
        start=start,
    ).stack()

    # give names to multi-index
    df.index.names = ["date", "symbol"]
    # make column names lower case
    df.columns = df.columns.str.lower()

    # compute atr_pct to use as filter later
    df["atr_pct"] = df.groupby(level=1, group_keys=False).apply(calculate_atr)

    # loop through
    for symbol in constituents.index.to_list():
        constituents.at[symbol, "atr_pct"] = df.xs(
            key=symbol, level="symbol"
        ).iloc[-1]["atr_pct"]

        start_price = df.xs(key=symbol, level="symbol").iloc[0]["close"]
        end_price = df.xs(key=symbol, level="symbol").iloc[-1]["close"]
        constituents.at[symbol, "change"] = (
            end_price - start_price
        ) / start_price

    outperformers = constituents[
        (constituents["change"] > sp500_change)
        & (constituents["atr_pct"] >= 2)
        & (constituents["atr_pct"] <= 3)
    ]
    outperformers = outperformers.reset_index()

    outperformers = outperformers.sort_values(by="change", ascending=False)

    return outperformers.to_dict(orient="records")

    # don't forget that you already download 52 week weekly ohlc here
    # return {"outperformers": outperformers, "df": df}
    # return outperformers.to_json(orient="records")
