from bson import ObjectId

from app.server.db.client import db
from app.server.models.bot import BotSchemaDb
from app.server.utils.common import clean_dict_helper, form_query

bot_user_collection = db['bot']


def bot_helper(bot):
    results = {
        **bot,
        "id": str(bot["_id"]),
    }
    return clean_dict_helper(results)


async def get_bot_from_db(abbr: str) -> BotSchemaDb:
    query = {"abbreviation": abbr, "is_active": True}
    print(query)
    async for bot in bot_user_collection.find(query):
        return BotSchemaDb(**bot_helper(bot))
