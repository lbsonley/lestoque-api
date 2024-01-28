from pydantic import ConfigDict, BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from enum import Enum
from .id import PyObjectId


class TradeDirections(str, Enum):
    long = "long"
    short = "short"


class TradeModel(BaseModel):
    """
    Container for a single trade record.
    """

    # The primary key for the TradeModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    symbol: Optional[str] = Field(default=None)
    direction: Optional[TradeDirections] = Field(default=None)
    portfolioValue: Optional[float] = Field(default=None)
    entry: Optional[float] = Field(default=None)
    stop: Optional[float] = Field(default=None)
    target: Optional[float] = Field(default=None)
    shares: Optional[float] = Field(default=None)
    ratio: Optional[float] = Field(default=None)
    risk: Optional[float] = Field(default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "symbol": "EXPE",
                "direction": "long",
                "portfolioValue": 4200,
                "entryPrice": 120.25,
                "stopPrice": 119.00,
                "targetPrice": 130.75,
                "shares": 80,
                "ratio": 8.4,
                "risk": 32,
            }
        },
    )


class TradeCollection(BaseModel):
    """
    A container holding a list of `TradeModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    items: List[TradeModel]
