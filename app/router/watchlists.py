from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..db.models.watchlist import WatchlistCollection
from ..db.connection import (
    db,
    outperformers_collection,
    etfs_collection,
    holdings_collection,
)

router = APIRouter()

collectionMap = {
    "outperformers": outperformers_collection,
    "etfs": etfs_collection,
    "holdings": holdings_collection,
}


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
