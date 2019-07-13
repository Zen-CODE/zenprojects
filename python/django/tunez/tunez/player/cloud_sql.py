"""
This module houses code that interacts with the CloudSQL Postgress instance
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import sessionmaker
from logging import getLogger
from os import environ

Base = declarative_base()
logger = getLogger(__name__)


class NowPlaying(Base):
    """
    This class defines the model mapping the 'Now Playing' entries to the
    database table.

    In order to create the tables:

        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)

    """
    # SQL Alchemy
    __tablename__ = 'now_playing'

    id = Column(Integer, primary_key=True)
    artist = Column(String)
    album = Column(String)
    state = Column(String)
    date = Column(Date)

    # Our properties
    Session = None

    @staticmethod
    def getSession():
        """ Return an instantiated Session object. """
        if NowPlaying.Session is None:
            engine = create_engine(
                environ['SQLALCHEMY_DATABASE_URI'],
                connect_args={'sslmode': 'prefer'})
            NowPlaying.Session = sessionmaker(bind=engine)
        return NowPlaying.Session()

    def __repr__(self):
        return "<NowPlaying(artist='{0}', album='{1}', state='{2}'".format(
            self.artist, self.album, self.state)

    def save(self):
        """ Store the item in the database """
        logger.info("Storing 'Now Playing' entry...")
        session = self.getSession()
        session.add(self)
        session.commit()
        logger.info("Storing 'Now Playing' entry stored.")


if __name__ == "__main__":
    from datetime import datetime
    from environs import Env
    env = Env()
    env.read_env()

    # Save
    # obj = NowPlaying(artist="Us3", album="Cantaloop 2004", state="playing",
    #                  date=datetime.now())
    # obj.save()

    # Delete all
    # session = NowPlaying.getSession()
    # for instance in session.query(NowPlaying).order_by(NowPlaying.date):
    #     print("Now playing: {0}".format(instance))
    #     session.delete(instance)
    # session.commit()

    # List all
    session = NowPlaying.getSession()
    for instance in session.query(NowPlaying).order_by(NowPlaying.date)[:10]:
        print("Now playing: {0}".format(instance))
    print("Done")
