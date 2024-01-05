from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
import yfinance as yf
from ..db.models.industries import IndustryItemModel, IndustryCollection
from ..db.connection import industries_collection
from ..dependencies.performance import get_constituents_change

router = APIRouter()


@router.get(
    "/api/industries",
    response_class=JSONResponse,
    status_code=200,
)
async def load_industries():
    return IndustryCollection(
        items=await industries_collection.find()
        .sort({"qoqChange": -1})
        .to_list(1000)
    )


@router.get(
    "/cron/industries",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_industries(start: str, end: str):
    constituents = pd.read_csv(
        filepath_or_buffer="app/db/static/industries.csv", index_col="symbol"
    )

    industries = await get_constituents_change(constituents, start, end)

    inserted_ids = []

    await industries_collection.drop()

    for etf in industries:
        model = IndustryItemModel(
            symbol=etf["symbol"],
            name=etf["name"],
            sector=etf["sector"],
            atrPct=etf["atr_pct"],
            qoqChange=etf["qoq_change"],
            yoyChange=etf["yoy_change"],
        )

        db_result = await industries_collection.insert_one(
            model.model_dump(by_alias=True, exclude=["id"])
        )
        inserted_ids.append(db_result.inserted_id)

    return industries


@router.get(
    "/cron/industry-constituents",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_industry_constituents():
    constituents = pd.read_csv(
        "https://www.ishares.com/us/products/239771/ishares-north-american-techsoftware-etf/1467271812596.ajax?fileType=csv&fileName=IGV_holdings&dataType=fund"
    )

    return constituents.to_dict(orient="records")
