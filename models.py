from sqlalchemy import create_engine, Column, Integer, Unicode, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker, scoped_session, synonym
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

engine = create_engine(
    "postgresql+psycopg2:///sql_test:sql_test@localhost:5432/sql_test", echo=True
)
if not database_exists(engine.url):
    create_database(engine.url)
DeclarativeBase = declarative_base()

maker = sessionmaker(autoflush=True, autocommit=False)
DBSession = scoped_session(maker)
DBSession.configure(bind=engine)


class Parent(DeclarativeBase):
    __tablename__ = "parent_table"

    id = Column(Integer, autoincrement=True, primary_key=True)
    json_column = Column(JSONB, nullable=False, default={})
    aliased_json_column = synonym("json_column")
    type = Column(Unicode, nullable=False)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "parent",
    }


class Child(Parent):
    __tablename__ = "child_table"

    child_id = Column(Integer, ForeignKey("parent_table.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "child"}


DeclarativeBase.metadata.create_all(engine)