from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)
    faction = Column(String(250), nullable=True)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    faction = Column(String(250), nullable=True)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///data/database/warbot.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
