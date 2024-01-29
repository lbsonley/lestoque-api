from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
from ..db.models.watchlist import WatchlistItemModel
from ..db.connection import holdings_collection
from ..dependencies.performance import get_constituents_change

router = APIRouter()

holdings = pd.read_csv(
    filepath_or_buffer="app/db/static/holdings.csv", index_col="symbol"
)


@router.get(
    "/cron/holdings",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_holdings(start: str, end: str):
    securities = await get_constituents_change(
        constituents=holdings,
        start=start,
        end=end,
        atr_cutoff=0.0,
        vol_cutoff=0.0,
    )

    await holdings_collection.drop()

    for holding in securities:
        model = WatchlistItemModel(
            symbol=holding["symbol"],
            name=holding["name"],
            atrPct=holding["atr_pct"],
            qoqChange=holding["qoq_change"],
            yoyChange=holding["yoy_change"],
        )

        await holdings_collection.insert_one(
            model.model_dump(by_alias=True, exclude=["id"])
        )

    return securities
