from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
from ..db.models.watchlist import WatchlistItemModel
from ..db.connection import industries_collection, industry_collections
from ..dependencies.performance import get_constituents_change
from ..dependencies.constituents import get_industry_constituents

router = APIRouter()

industry_etfs = pd.read_csv(
    filepath_or_buffer="app/db/static/industries.csv", index_col="symbol"
)


@router.get(
    "/cron/industries",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_industries(start: str, end: str):
    industries = await get_constituents_change(industry_etfs, start, end)

    await industries_collection.drop()

    for etf in industries:
        model = WatchlistItemModel(
            symbol=etf["symbol"],
            name=etf["name"],
            atrPct=etf["atr_pct"],
            qoqChange=etf["qoq_change"],
            yoyChange=etf["yoy_change"],
        )

        await industries_collection.insert_one(
            model.model_dump(by_alias=True, exclude=["id"])
        )

    return industries


@router.get(
    "/cron/industry-constituents",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_industry_constituents(start: str, end: str):
    for symbol in industry_etfs.index.to_list():
        print(symbol)
        await industry_collections[symbol].drop()

        constituents = await get_industry_constituents(symbol)

        constituent_spec = await get_constituents_change(
            constituents, start, end
        )

        for stock in constituent_spec:
            model = WatchlistItemModel(
                symbol=stock["symbol"],
                name=stock["name"],
                atrPct=stock["atr_pct"],
                qoqChange=stock["qoq_change"],
                yoyChange=stock["yoy_change"],
            )

            await industry_collections[symbol].insert_one(
                model.model_dump(by_alias=True, exclude=["id"])
            )

    return {"foo": "bar"}
