import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


class DataAccessObject:
    @classmethod
    def execute(cls, query, params=None):
        return db.execute(query, params)

    @classmethod
    def rowcount(cls, query, params):
        return DataAccessObject.execute(query, params).rowcount

    @classmethod
    def fetchone(cls, query, params=None):
        return DataAccessObject.execute(query, params).fetchone()

    @classmethod
    def fetchall(cls, query, params=None):
        return DataAccessObject.execute(query, params).fetchall()

    @classmethod
    def alter(cls, query, params=None):
        DataAccessObject.execute(query, params)
        db.commit()
