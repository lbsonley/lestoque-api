from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..db.models.watchlist import WatchlistItemModel
from ..db.connection import outperformers_collection
from ..dependencies.performance import get_constituents_change
from ..dependencies.constituents import get_sp_500_constituents

router = APIRouter()


@router.get(
    "/cron/outperformers",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_outperformers(start: str, end: str):
    sp_500_constituents = await get_sp_500_constituents()
    outperformers: List[WatchlistItemModel] = await get_constituents_change(
        constituents=sp_500_constituents,
        start=start,
        end=end,
        atr_cutoff=2.0,
        vol_cutoff=4e6,
    )

    inserted_ids = []

    await outperformers_collection.drop()

    for stock in outperformers:
        model = WatchlistItemModel(
            symbol=stock["symbol"],
            name=stock["name"],
            sector=stock["sector"],
            subIndustry=stock["subIndustry"],
            atrPct=stock["atr_pct"],
            qoqChange=stock["qoq_change"],
            yoyChange=stock["yoy_change"],
        )

        db_result = await outperformers_collection.insert_one(
            model.model_dump(by_alias=True, exclude=["id"])
        )
        inserted_ids.append(db_result.inserted_id)

    return outperformers
