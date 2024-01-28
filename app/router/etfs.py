from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
from ..db.models.watchlist import WatchlistItemModel
from ..db.connection import etfs_collection
from ..dependencies.performance import get_constituents_change

router = APIRouter()

etfs = pd.read_csv(
    filepath_or_buffer="app/db/static/etfs.csv", index_col="symbol"
)


@router.get(
    "/cron/etfs",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_etfs(start: str, end: str):
    securities = await get_constituents_change(etfs, start, end, False)

    await etfs_collection.drop()

    for etf in securities:
        model = WatchlistItemModel(
            symbol=etf["symbol"],
            name=etf["name"],
            atrPct=etf["atr_pct"],
            qoqChange=etf["qoq_change"],
            yoyChange=etf["yoy_change"],
        )

        await etfs_collection.insert_one(
            model.model_dump(by_alias=True, exclude=["id"])
        )

    return securities
