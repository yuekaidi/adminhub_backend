from datetime import datetime
from re import escape

from bson import Regex

from app.server.db.client import db
from app.server.models.question import QuestionSchema
from app.server.utils.common import clean_dict_helper, form_query

question_user_collection = db['question']


def question_helper(question) -> dict:
    return {
        **question,
        "id": str(question["_id"]),
        "created_by": str(question["created_by"]),
        "updated_by": str(question["updated_by"]),
        "answers": clean_dict_helper(question["answers"])
    }


async def get_questions_from_db(*, current_page: int, page_size: int, sorter=None, question_text: str,
                                language: str, topic: str, created_at: datetime) -> list[QuestionSchema]:
    sort = []
    if sorter:
        # [("answers", 1), ("bot_user_group", 1)]
        for key, value in sorter:
            order = 1 if value == 'ascend' else -1
            sort.append((key, order))
        print(sort)

    db_key = [("topic", topic),
              (f"text.{language}", Regex(f".*{escape(question_text)}.*", "i") if question_text else None),
              ("created_at", created_at)]

    query = form_query(db_key)

    print(query)
    cursor = question_user_collection.find(query)
    cursor.skip((current_page - 1) * page_size).limit(page_size)
    questions = []
    async for question in cursor:
        questions.append(QuestionSchema(**question_helper(question)))
    return questions
