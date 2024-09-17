from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Nationality(Base):
    __tablename__ = "nationalities"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Championship(Base):
    __tablename__ = "championships"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nationality_id = Column(Integer, ForeignKey("nationalities.id"))
    nationality = relationship("Nationality")


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    nationality_id = Column(Integer, ForeignKey("nationalities.id"))
    nationality = relationship("Nationality")

    # Relationships
    matches = relationship(
        "Match", back_populates="player", foreign_keys="Match.player_id"
    )
    trophies = relationship("Trophy", back_populates="player")

    # New columns for highest scoring match and trophies won
    highest_scoring_match_id = Column(Integer, ForeignKey("matches.id"), nullable=True)
    trophies_won = Column(Integer, default=0)


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    championship_id = Column(Integer, ForeignKey("championships.id"))
    player_id = Column(Integer, ForeignKey("players.id"))  # Foreign key to Player
    frames_won = Column(Integer, nullable=False)
    frames_lost = Column(Integer, nullable=False)
    total_points = Column(Integer, nullable=False)

    # Relationships
    player = relationship("Player", back_populates="matches", foreign_keys=[player_id])
    championship = relationship("Championship")


class Trophy(Base):
    __tablename__ = "trophies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"))  # Foreign key to Player
    player = relationship("Player", back_populates="trophies")


# Create an SQLite database in memory for testing
engine = create_engine("sqlite:///snooker.db")
Base.metadata.create_all(engine)
