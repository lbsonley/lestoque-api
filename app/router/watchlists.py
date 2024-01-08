from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..db.models.watchlist import WatchlistItemModel, WatchlistCollection
from ..db.connection import (
    db,
    outperformers_collection,
    industries_collection,
    industry_collections,
)
from ..dependencies.performance import get_constituents_change
from ..dependencies.constituents import get_sp_500_constituents

router = APIRouter()

collectionMap = {
    "outperformers": outperformers_collection,
    "industries": industries_collection,
    **industry_collections,
}


@router.get(
    "/api/watchlist-names",
    response_class=JSONResponse,
    status_code=200,
)
async def load_watchlist_names():
    filter = {"name": {"$regex": r"^(?!system\.)"}}
    names = await db.list_collection_names(filter=filter)
    return names


@router.get(
    "/api/watchlists",
    response_class=JSONResponse,
    status_code=200,
)
async def load_watchlist(list_name):
    return WatchlistCollection(
        items=await collectionMap[list_name]
        .find()
        .sort({"qoqChange": -1})
        .to_list(1000)
    )
