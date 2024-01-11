from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
from ..db.models.watchlist import WatchlistItemModel
from ..db.connection import indices_collection
from ..dependencies.performance import get_constituents_change

router = APIRouter()

index_etfs = pd.read_csv(
    filepath_or_buffer="app/db/static/indices.csv", index_col="symbol"
)


@router.get(
    "/cron/indices",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_indices(start: str, end: str):
    indices = await get_constituents_change(index_etfs, start, end, False)

    await indices_collection.drop()

    for etf in indices:
        model = WatchlistItemModel(
            symbol=etf["symbol"],
            name=etf["name"],
            atrPct=etf["atr_pct"],
            qoqChange=etf["qoq_change"],
            yoyChange=etf["yoy_change"],
        )

        await indices_collection.insert_one(
            model.model_dump(by_alias=True, exclude=["id"])
        )

    return indices
