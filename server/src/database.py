import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///soccer_management.db')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


class PlayerModel(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    number = Column(Integer)
    team_name = Column(String, ForeignKey('teams.name'))
    position = Column(String)
    is_starting = Column(Boolean)
    goals = Column(Integer, default=0)

    team = relationship("TeamModel", back_populates="players")


class TeamModel(Base):
    __tablename__ = 'teams'

    name = Column(String, primary_key=True, index=True)
    total_goals = Column(Integer, default=0)
    conceded_goals = Column(Integer, default=0)
    points = Column(Integer, default=0)
    group = Column(String, default='')

    players = relationship("PlayerModel", back_populates="team")


class MatchModel(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, index=True)
    round = Column(Integer)
    teams = Column(JSON)
    scores = Column(JSON)
    date = Column(String)
    stadium = Column(String)
    localization = Column(JSON)
    scorers = Column(JSON)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
