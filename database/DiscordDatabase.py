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


engine = create_engine('sqlite:///data/database/warbot.db')

Base.metadata.create_all(engine)
