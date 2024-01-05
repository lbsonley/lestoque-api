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
