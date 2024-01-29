import yfinance as yf
import pandas_ta as ta
from .atr import calculate_atr


# TODO => Retry fetching symbols that fail
# https://github.com/ranaroussi/yfinance/issues/359


async def get_sp_500_change(start: str, end: str):
    sp500 = yf.download(tickers=["SPY"], start=start, end=end)

    sp500.index.names = ["datetime"]
    sp500.columns = sp500.columns.str.lower()

    sp500_change = (
        sp500.iloc[-1]["close"] - sp500.iloc[0]["close"]
    ) / sp500.iloc[0]["close"]

    return sp500_change


async def get_constituents_change(
    constituents,
    start,
    end,
    atr_cutoff=0.5,
    vol_cutoff=1e6,
):
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
    df["vol_ma"] = df.groupby(level=1, group_keys=False).apply(
        lambda x: ta.sma(x.volume, length=50)
    )

    # loop through
    for symbol in constituents.index.to_list():
        constituents.at[symbol, "atr_pct"] = df.xs(
            key=symbol, level="symbol"
        ).iloc[-1]["atr_pct"]

        constituents.at[symbol, "vol_ma"] = df.xs(
            key=symbol, level="symbol"
        ).iloc[-1]["vol_ma"]

        qoq_index = -65
        if len(df.xs(key=symbol, level="symbol")) < 65:
            qoq_index = -1

        yoy_price = df.xs(key=symbol, level="symbol").iloc[0]["close"]
        qoq_price = df.xs(key=symbol, level="symbol").iloc[qoq_index]["close"]
        end_price = df.xs(key=symbol, level="symbol").iloc[-1]["close"]
        constituents.at[symbol, "yoy_change"] = (
            end_price - yoy_price
        ) / yoy_price
        constituents.at[symbol, "qoq_change"] = (
            end_price - qoq_price
        ) / qoq_price

    constituents = constituents.reset_index()

    constituents = constituents[constituents["vol_ma"] > vol_cutoff]

    constituents = constituents[constituents["atr_pct"] > atr_cutoff]

    constituents = constituents.sort_values(by="yoy_change", ascending=False)

    return constituents.to_dict(orient="records")
