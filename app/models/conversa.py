from bson import ObjectId
from datetime import datetime, timezone

def create_talk(db, title="Nova conversa"):
    result = db.conversas.insert_one({
        'title': title,
        'created_on': datetime.now(timezone.utc),
        'messages': []
    })
    return str(result.inserted_id)

def serch_talk(db, talk_id):
    return db.conversas.find_one({"_id": ObjectId(talk_id)})
    

def update_talk(db, talk_id, role, content):
    db.conversas.upadte_one(
        {"_id": ObjectId(talk_id)},
        {"$push": {"messages": {"role": role, "content": content}}}
    )
    