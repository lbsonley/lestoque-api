from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..db.models.outperformers import WatchlistItemModel, WatchlistCollection
from ..db.connection import outperformers_collection
from ..dependencies.performance import get_sp_500_change, get_outperformers

router = APIRouter()


@router.get(
    "/api/outperformers",
    response_class=JSONResponse,
    status_code=200,
)
async def load_outperformers():
    return WatchlistCollection(
        items=await outperformers_collection.find().to_list(1000)
    )


@router.get(
    "/cron/outperformers",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_outperformers():
    sp_500_change = await get_sp_500_change("2023-09-28", "2023-12-29")
    outperformers: List[WatchlistItemModel] = await get_outperformers(
        "2023-09-28", "2023-12-29", sp_500_change
    )

    inserted_ids = []

    outperformers_collection.drop()

    for stock in outperformers:
        model = WatchlistItemModel(
            symbol=stock["symbol"],
            name=stock["name"],
            sector=stock["sector"],
            subIndustry=stock["subIndustry"],
            atrPct=stock["atr_pct"],
            change=stock["change"],
        )

        db_result = await outperformers_collection.insert_one(
            model.model_dump(by_alias=True, exclude=["id"])
        )
        inserted_ids.append(db_result.inserted_id)

    return outperformers