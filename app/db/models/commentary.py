from pydantic import ConfigDict, BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from .id import PyObjectId
from datetime import datetime


class CommentaryModel(BaseModel):
    """
    Container for a single commentary record.
    """

    # The primary key for the CommentaryModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    symbol: Optional[str] = Field(default=None)
    dt: Optional[datetime] = Field(default=None)
    monthly: Optional[str] = Field(default=None)
    weekly: Optional[str] = Field(default=None)
    daily: Optional[str] = Field(default=None)
    ninetyMin: Optional[str] = Field(default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "symbol": "EXPE",
                "datetime": "1706387852172",
                "monthly": "foo bar baz",
                "weekly": "foo bar baz",
                "daily": "foo bar baz",
                "ninetyMin": "foo bar baz",
            }
        },
    )


class CommentaryCollection(BaseModel):
    """
    A container holding a list of `CommentaryModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    items: List[CommentaryModel]
