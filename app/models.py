from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    founded_year = Column(Integer, nullable=False)
    stadium = Column(String, nullable=False)
    coach_name = Column(String, nullable=False)

    players = relationship("Player", back_populates="team")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    age = Column(Integer)
    nationality = Column(String)
    position = Column(String)
    shirt_number = Column(Integer)
    team_id = Column(Integer, ForeignKey("teams.id"))
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    appearances = Column(Integer, default=0)

    team = relationship("Team", back_populates="players")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    match_date = Column(String)
    competition = Column(String)
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    venue = Column(String)
    status = Column(String)