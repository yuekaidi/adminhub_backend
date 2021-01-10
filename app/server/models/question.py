from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel


class QuestionVariationSchema(BaseModel):
    id: str
    text: str
    language: str
    internal: bool


class QuestionAnswerSchema(BaseModel):
    id: str
    flow: dict
    bot_user_group: Optional[str]


class QuestionSchema(BaseModel):
    id: str
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    text: dict
    internal: bool
    keyword: Optional[list[str]]
    answers: list[QuestionAnswerSchema]
    alternate_questions: list[QuestionVariationSchema]
    topic: str
    active_at: Optional[datetime]
    expire_at: Optional[datetime]
    is_active: bool

    class Config:
        schema_extra = {
            "example": {
                "_id": ObjectId("5fe14e41d0c0a70910280174"),
                "created_at": datetime.now(),
                "created_by": ObjectId("5e6217be51cc760b8677707e"),
                "updated_at": datetime.now(),
                "updated_by": ObjectId("5e6217be51cc760b8677707e"),
                "text": {
                    "EN": "Christmas e-card"
                },
                "internal": True,
                "keyword": ['a', 'b', 'c'],
                "answers": [
                    {
                        "id": "1",
                        "flow": {
                            "flow_id": ObjectId("5fe14d8dd0c0a7091028015c")
                        },
                        "bot_user_group": "1"
                    }
                ],
                "alternate_questions": [
                    {
                        "id": "a11b2322-e0e1-421c-b187-a96e1c9b4c37",
                        "text": "Merry Xmas greeting card",
                        "language": "EN",
                        "internal": False
                    },
                ],
                "topic": "Christmas e-Card",
                "active_at": None,
                "expire_at": None,
                "is_active": False
            }
        }
