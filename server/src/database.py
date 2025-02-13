import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, JSON, ARRAY
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:admin@localhost:5432/tournament_db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


class PlayerModel(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    number = Column(Integer)
    team_id = Column(Integer, ForeignKey('teams.id'))
    position = Column(String)
    is_starting = Column(Boolean)
    goals = Column(Integer, default=0)

    team = relationship("TeamModel", back_populates="players")


class TeamModel(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    total_goals = Column(Integer, default=0)
    conceded_goals = Column(Integer, default=0)
    points = Column(Integer, default=0)
    group = Column(String, default='')

    players = relationship("PlayerModel", back_populates="team")


class MatchModel(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, index=True)
    round = Column(Integer)
    team1_id = Column(Integer, ForeignKey('teams.id'))
    team2_id = Column(Integer, ForeignKey('teams.id'))
    score1 = Column(Integer)
    score2 = Column(Integer)
    date = Column(String)
    stadium = Column(String)
    localization = Column(JSON)
    scorers1 = Column(ARRAY(JSON))
    scorers2 = Column(ARRAY(JSON))

    team1 = relationship("TeamModel", foreign_keys=[team1_id])
    team2 = relationship("TeamModel", foreign_keys=[team2_id])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
