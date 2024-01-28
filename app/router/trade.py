from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from ..db.models.trade import TradeModel
from ..db.connection import trades_collection

router = APIRouter()


@router.get(
    "/api/trade",
    response_description="get trade",
    response_model=TradeModel,
    response_class=JSONResponse,
    status_code=200,
)
async def get_trade(symbol: str):
    trade = await trades_collection.find_one({"symbol": symbol})
    if trade:
        return trade
    else:
        return {}


@router.post(
    "/api/trade",
    response_description="Add new trade",
    response_model=TradeModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def post_trade(symbol: str, trade: TradeModel):
    old_trade = await trades_collection.find_one({"symbol": symbol})

    if old_trade is not None:
        new_trade = await trades_collection.replace_one(
            {"symbol": symbol},
            trade.model_dump(by_alias=True, exclude=["id"]),
        )
    else:
        new_trade = await trades_collection.insert_one(
            trade.model_dump(by_alias=True, exclude=["id"])
        )

    created_trade = await trades_collection.find_one({"symbol": symbol})
    return created_trade
