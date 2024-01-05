from pydantic import ConfigDict, BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from .id import PyObjectId


class IndustryItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    symbol: str = Field(...)
    name: str = Field(...)
    sector: str = Field(default=None)
    atrPct: float = Field(default=None)
    qoqChange: float = Field(default=None)
    yoyChange: float = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "symbol": "ITB",
                "name": "Home Construction",
                "sector": "Consumer Discretionary",
                "atrPct": 2.554,
                "qoqChange": 0.154,
                "yoyChange": 0.554,
            }
        },
    )


class IndustryCollection(BaseModel):
    """
    A container holding a list of `IndustryItemModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    items: List[IndustryItemModel]
