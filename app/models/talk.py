from bson import ObjectId
from datetime import datetime, timezone

def create_talk(db, title="Nova conversa"):
    result = db.conversas.insert_one({
        'title': title,
        'created_on': datetime.now(timezone.utc),
        'message': []
    })
    return str(result.inserted_id)

def search_talk(db, talk_id):
    return db.conversas.find_one({"_id": ObjectId(talk_id)})
    

def add_message(db, talk_id, role, content):
    db.conversas.update_one(
        {"_id": ObjectId(talk_id)},
        {"$push": {'message': {"role": role, "content": content}}}
    )
    