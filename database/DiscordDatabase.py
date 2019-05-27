from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)
    faction = Column(String(250), nullable=True, default="NULL")
    claimer = Column(String(250), nullable=True, default="NULL")
    terran = Column(Integer, name="Terran Members", default=0)
    protoss = Column(Integer, name="Protoss Members", default=0)
    zerg = Column(Integer, name="Zerg Members", default=0)
    marines = Column(Integer, name="Marine Members", default=0)
    yautja = Column(Integer, name="Yautja Members", default=0)
    xenomorphs = Column(Integer, name="Xenomorph Members", default=0)
    unsc = Column(Integer, name="UNSC Members", default=0)
    covenant = Column(Integer, name="Covenant Members", default=0)
    flood = Column(Integer, name="Flood Members", default=0)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    faction = Column(String(250), nullable=True)


class Terran(Base):
    __tablename__ = 'terran'

    id = Column(Integer, primary_key=True)
    minerals = Column(Integer, name='Minerals', nullable=False, default=0)
    vespene = Column(Integer, name='Vespene', nullable=False, default=0)


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


class Zerg(Base):
    __tablename__ = 'zerg'

    id = Column(Integer, primary_key=True)
    minerals = Column(Integer, name='Minerals', nullable=False, default=0)
    vespene = Column(Integer, name='Vespene', nullable=False, default=0)


engine = create_engine('sqlite:///data/database/warbot.db')

Base.metadata.create_all(engine)
