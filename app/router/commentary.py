from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from ..db.models.commentary import CommentaryModel
from ..db.connection import commentary_collection

router = APIRouter()


@router.get(
    "/api/commentary",
    response_description="get commentary",
    response_model=CommentaryModel,
    response_class=JSONResponse,
    status_code=200,
)
async def get_commentary(symbol: str):
    commentary = await commentary_collection.find_one({"symbol": symbol})
    if commentary:
        return commentary
    else:
        return {
            "monthly": "",
            "weekly": "",
            "daily": "",
            "ninetyMin": "",
        }


@router.post(
    "/api/commentary",
    response_description="Add new commentary",
    response_model=CommentaryModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def post_commentary(symbol: str, commentary: CommentaryModel):
    old_commentary = await commentary_collection.find_one({"symbol": symbol})

    if old_commentary is not None:
        new_commentary = await commentary_collection.replace_one(
            {"symbol": symbol},
            commentary.model_dump(by_alias=True, exclude=["id"]),
        )
    else:
        new_commentary = await commentary_collection.insert_one(
            commentary.model_dump(by_alias=True, exclude=["id"])
        )

    created_commentary = await commentary_collection.find_one(
        {"symbol": symbol}
    )
    return created_commentary
