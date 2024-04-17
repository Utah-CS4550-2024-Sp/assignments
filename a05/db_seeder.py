import json

from sqlalchemy import func
from sqlmodel import Session, create_engine, select

from backend.schema import *
from backend.database import engine

SQLModel.metadata.create_all(engine)

local_engine = create_engine(
    "sqlite:///backend/initial.db",
    connect_args={"check_same_thread": False},
)


def upsert_all(session, cls, local_models) -> int:
    models = session.exec(select(cls)).all()
    model_lookup = {model.id: model for model in models}
    count = 0
    for local_model in local_models:
        if model_lookup.get(local_model.id) is None:
            session.add(cls(**{
                key: value
                for key, value in local_model.model_dump().items()
                if key != "id"
            }))
            count += 1
    session.commit()
    return count


def upsert_links(session, local_models) -> int:
    links = session.exec(select(UserChatLinkInDB)).all()
    link_lookup = {(link.user_id, link.chat_id): link for link in links}
    count = 0
    for local_model in local_models:
        if link_lookup.get((local_model.user_id, local_model.chat_id)) is None:
            session.add(UserChatLinkInDB(**local_model.model_dump()))
            count += 1
    session.commit()
    return count


def get_count(session, model):
    if model == UserChatLinkInDB:
        return session.scalar(select(func.count(model.user_id)))
    return session.scalar(select(func.count(model.id)))


def add_users() -> dict[str, int]:
    with Session(local_engine) as local_session:
        users = local_session.exec(select(UserInDB)).all()
        local_count = len(users)

    with Session(engine) as session:
        prev_count = get_count(session, UserInDB)
        additions = upsert_all(session, UserInDB, users)
        count = get_count(session, UserInDB)

    return {
        "local": local_count,
        "prev": prev_count,
        "additions": additions,
        "final": count,
    }


def add_chats() -> dict[str, int]:
    with Session(local_engine) as local_session:
        chats = local_session.exec(select(ChatInDB)).all()
        local_count = len(chats)

    with Session(engine) as session:
        prev_count = get_count(session, ChatInDB)
        additions = upsert_all(session, ChatInDB, chats)
        count = get_count(session, ChatInDB)

    return {
        "local": local_count,
        "prev": prev_count,
        "additions": additions,
        "final": count,
    }


def add_messages() -> dict[str, int]:
    with Session(local_engine) as local_session:
        messages = local_session.exec(select(MessageInDB)).all()
        local_count = len(messages)

    with Session(engine) as session:
        prev_count = get_count(session, MessageInDB)
        additions = upsert_all(session, MessageInDB, messages)
        count = get_count(session, MessageInDB)

    return {
        "local": local_count,
        "prev": prev_count,
        "additions": additions,
        "final": count,
    }


def add_user_chat_links() -> dict[str, int]:
    with Session(local_engine) as local_session:
        links = local_session.exec(select(UserChatLinkInDB)).all()
        local_count = len(links)

    with Session(engine) as session:
        prev_count = get_count(session, UserChatLinkInDB)
        additions = upsert_links(session, links)
        count = get_count(session, UserChatLinkInDB)

    return {
        "local": local_count,
        "prev": prev_count,
        "additions": additions,
        "final": count,
    }


def seed_database():
    user_count = add_users()
    chat_count = add_chats()
    message_count = add_messages()
    link_count = add_user_chat_links()

    return {
        "user_count": user_count,
        "chat_count": chat_count,
        "message_count": message_count,
        "link_count": link_count,
    }


def lambda_handler(event, context):
    try:
        result = seed_database()
        return {
            "statusCode": 200,
            "body": json.dumps(result),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }


if __name__ == "__main__":
    seed_database()

