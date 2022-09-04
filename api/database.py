from sqlmodel import SQLModel, Session, create_engine

from api.config import get_settings


connect_args = {"check_same_thread": False}
engine = create_engine(get_settings().DATABASE_URI, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
