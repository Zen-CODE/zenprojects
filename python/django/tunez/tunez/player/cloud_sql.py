"""
This module houses code that interacts with the CloudSQL Postgress instance
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from os import environ


Base = declarative_base()


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
    track = Column(String)
    state = Column(String)
    machine = Column(String)
    datetime = Column(DateTime)

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
            # Base.metadata.create_all(engine)
        return NowPlaying.Session()

    def __repr__(self):
        return "<NowPlaying on {5}: {0},  {1}: {2}, state={3} @{4}".format(
            self.artist, self.album, self.track, self.state, self.datetime,
            self.machine)

    def save(self):
        """ Store the item in the database """
        _session = self.getSession()
        _session.add(self)
        _session.commit()


if __name__ == "__main__":
    from environs import Env
    env = Env()
    env.read_env()

    # Save
    # from datetime import datetime
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
    for instance in session.query(
            NowPlaying).order_by(NowPlaying.datetime.desc())[:10]:
        print("Now playing: {0}".format(instance))
    print("Done")
