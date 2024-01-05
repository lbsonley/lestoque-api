from pydantic import ConfigDict, BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from .id import PyObjectId


class WatchlistItemModel(BaseModel):
    """
    Container for a single watchlist item record.
    """

    # The primary key for the WatchlistItemModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    symbol: str = Field(...)
    name: str = Field(...)
    sector: str = Field(default=None)
    subIndustry: str = Field(default=None)
    atrPct: float = Field(default=None)
    qoqChange: float = Field(default=None)
    yoyChange: float = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "symbol": "EXPE",
                "name": "Expedia",
                "sector": "Consumer Discretionary",
                "subIndustry": "Hotels, Resorts & Cruise Lines",
                "atrPct": 2.554,
                "qoqChange": 0.154,
                "yoyChange": 0.554,
            }
        },
    )


class WatchlistCollection(BaseModel):
    """
    A container holding a list of `WatchlistItemModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    items: List[WatchlistItemModel]
