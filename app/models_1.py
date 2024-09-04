from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    first_login = Column(DateTime, default=func.now())
    boosts = relationship('Boost', back_populates='player')


class Boost(Base):
    __tablename__ = 'boosts'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship('Player', back_populates='boosts')
    awarded_for_level = Column(Boolean, default=False)
