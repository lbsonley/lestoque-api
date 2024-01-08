import pandas as pd


async def get_sp_500_constituents():
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

    return constituents


async def get_industry_constituents(symbol: str):
    tables = pd.read_html(f"https://etfdb.com/etf/{symbol}/#holdings")

    constituents_table_idx = -1
    for i in range(len(tables)):
        if "Symbol Symbol" in tables[i].columns:
            constituents_table_idx = i

    constituents_table_idx

    df = tables[constituents_table_idx]
    df = df[["Symbol Symbol", "Holding Holding"]]
    df.columns = ["symbol", "name"]
    df.index = df["symbol"]
    df.index = df.index.str.replace(".", "-")
    df = df[["name"]]
    df = df.iloc[0:-1]
    return df
