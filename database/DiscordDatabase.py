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


class Protoss(Base):
    __tablename__ = 'protoss'

    id = Column(Integer, primary_key=True)
    minerals = Column(Integer, name='Minerals', nullable=False, default=0)
    vespene = Column(Integer, name='Vespene', nullable=False, default=0)
    # probe = Column(Integer, name='Probes', nullable=False, default=0)
    # zealot = Column(Integer, name='Zealots', nullable=False, default=0)
    # stalker = Column(Integer, name='Stalkers', nullable=False, default=0)
    # adept = Column(Integer, name='Adepts', nullable=False, default=0)
    # high_templar = Column(Integer, name='High Templars', nullable=False, default=0)


engine = create_engine('sqlite:///data/database/warbot.db')

Base.metadata.create_all(engine)
