from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
from ..db.models.watchlist import WatchlistItemModel
from ..db.connection import sectors_collection
from ..dependencies.performance import get_constituents_change

router = APIRouter()

sector_etfs = pd.read_csv(
    filepath_or_buffer="app/db/static/sectors.csv", index_col="symbol"
)


@router.get(
    "/cron/sectors",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_sectors(start: str, end: str):
    sectors = await get_constituents_change(sector_etfs, start, end)

    await sectors_collection.drop()

    for etf in sectors:
        model = WatchlistItemModel(
            symbol=etf["symbol"],
            name=etf["name"],
            atrPct=etf["atr_pct"],
            qoqChange=etf["qoq_change"],
            yoyChange=etf["yoy_change"],
        )

        await sectors_collection.insert_one(
            model.model_dump(by_alias=True, exclude=["id"])
        )

    return sectors
