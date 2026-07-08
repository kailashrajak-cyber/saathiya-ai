from models.user import db
from models.memory import UserMemory


def get_memory(user_id):
    memories = UserMemory.query.filter_by(user_id=user_id).all()
    return {m.key: m.value for m in memories}


def save_memory(user_id, key, value):
    memory = UserMemory.query.filter_by(
        user_id=user_id,
        key=key
    ).first()

    if memory:
        memory.value = value
    else:
        memory = UserMemory(
            user_id=user_id,
            key=key,
            value=value
        )
        db.session.add(memory)

    db.session.commit()


def delete_memory(user_id, key):
    memory = UserMemory.query.filter_by(
        user_id=user_id,
        key=key
    ).first()

    if memory:
        db.session.delete(memory)
        db.session.commit()
