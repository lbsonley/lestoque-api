from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..db.models.industries import IndustryItemModel, IndustryCollection
from ..db.connection import industries_collection

router = APIRouter()


@router.get(
    "/api/industries",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_industries():
    return IndustryCollection(
        items=await industries_collection.find().to_list(1000)
    )


@router.get(
    "/cron/industries",
    response_class=JSONResponse,
    status_code=200,
)
async def sync_industries():
    industries = [
        {
            "symbol": "IBB",
            "name": "Biotechnology",
            "sector": "Healthcare",
        },
        {
            "symbol": "IHF",
            "name": "Healthcare Providers",
            "sector": "Healthcare",
        },
        {
            "symbol": "IHI",
            "name": "Medical Devices",
            "sector": "Healthcare",
        },
        {
            "symbol": "IHE",
            "name": "Pharmaceuticals",
            "sector": "Healthcare",
        },
        {
            "symbol": "IEZ",
            "name": "Oil Equipment & Services",
            "sector": "Energy",
        },
        {
            "symbol": "IEO",
            "name": "Oil & Gas Exploration",
            "sector": "Energy",
        },
        {
            "symbol": "IGM",
            "name": "Expanded Tech",
            "sector": "Technology",
        },
        {
            "symbol": "SOXX",
            "name": "Semiconductors",
            "sector": "Technology",
        },
        {
            "symbol": "IGV",
            "name": "Tech Software",
            "sector": "Technology",
        },
        {
            "symbol": "IGN",
            "name": "Tech Multimedia",
            "sector": "Technology",
        },
        {
            "symbol": "ITA",
            "name": "Aerospace & Defense",
            "sector": "Industrials",
        },
        {
            "symbol": "IYT",
            "name": "Transportation",
            "sector": "Industrials",
        },
        {
            "symbol": "ITB",
            "name": "Home Construction",
            "sector": "Consumer Discretionary",
        },
        {
            "symbol": "IAI",
            "name": "Broker-Dealers & Securities Exchange",
            "sector": "Financials",
        },
        {
            "symbol": "IYG",
            "name": "Financial Services",
            "sector": "Financials",
        },
        {
            "symbol": "IYK",
            "name": "Insurance",
            "sector": "Financials",
        },
        {
            "symbol": "IAT",
            "name": "Regional Banks",
            "sector": "Financials",
        },
        {
            "symbol": "REM",
            "name": "Mortgage REITS",
            "sector": "Real Estate",
        },
        {
            "symbol": "REZ",
            "name": "Residential Real Estate",
            "sector": "Real Estate",
        },
        {
            "symbol": "ICOP",
            "name": "Copper & Metals Miners",
            "sector": "Materials",
        },
        {
            "symbol": "RING",
            "name": "Gold Miners",
            "sector": "Materials",
        },
        {
            "symbol": "ILIT",
            "name": "Lithium Miners & Producers",
            "sector": "Materials",
        },
        {
            "symbol": "PICK",
            "name": "Metal Producers & Miners",
            "sector": "Materials",
        },
        {
            "symbol": "SLVP",
            "name": "Silver Miners",
            "sector": "Materials",
        },
        {
            "symbol": "WOOD",
            "name": "Timber & Forestry",
            "sector": "Materials",
        },
    ]

    inserted_ids = []

    industries_collection.drop()

    for etf in industries:
        model = IndustryItemModel(
            symbol=etf["symbol"],
            name=etf["name"],
            sector=etf["sector"],
        )

        db_result = await industries_collection.insert_one(
            model.model_dump(by_alias=True, exclude=["id"])
        )
        inserted_ids.append(db_result.inserted_id)

    return industries
