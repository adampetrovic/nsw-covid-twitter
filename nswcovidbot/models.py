from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

from sqlalchemy import Table, Column, String, Integer, Date, ForeignKey, Float, DateTime, Numeric

Base = declarative_base()


class Tweet(Base):
    __tablename__ = "covid_tweets"
    id = Column(Integer, primary_key=True)
    tweet_id = Column(Numeric)
    venue_id = Column(Integer, ForeignKey('covid_venues.id', ondelete='CASCADE'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __init__(self, tweet_id, venue_id):
        self.tweet_id = tweet_id
        self.venue_id = venue_id


class Venue(Base):
    __tablename__ = "covid_venues"
    id = Column(Integer, primary_key=True)

    name = Column(String)
    address = Column(String)
    suburb = Column(String)
    date = Column(Date)
    time = Column(String)
    alert = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    last_update = Column(Date)

    tweet = relationship("Tweet", uselist=False, backref="tweet")

    def __init__(self, name, address, suburb, date, time, alert, latitude, longitude, last_update):
        self.name = name
        self.address = address
        self.suburb = suburb
        self.date = date
        self.time = time
        self.alert = alert
        self.latitude = latitude
        self.longitude = longitude
        self.last_update = last_update