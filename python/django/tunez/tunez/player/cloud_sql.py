"""
This module houses code that interacts with the CloudSQL Postgress instance
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import sessionmaker
from logging import getLogger


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

    def __init__(self, **kwargs):
        super(NowPlaying, self).__init__(**kwargs)
        if NowPlaying.Session is None:
            engine = create_engine(
                env('SQLALCHEMY_DATABASE_URI'),
                connect_args={'sslmode': 'prefer'})
            self.Session = sessionmaker(bind=engine)

    def __repr__(self):
        return "<NowPlaying(artist='{0}', album='{1}', state='{2}'".format(
            self.artist, self.album, self.state)

    def save(self):
        """ Store the item in the database """
        logger.info("Storing 'Now Playing' entry...")
        session = self.Session()
        session.add(self)
        session.commit()
        logger.info("Storing 'Now Playing' entry stored.")


if __name__ == "__main__":
    from datetime import datetime
    from environs import Env
    env = Env()
    env.read_env()

    obj = NowPlaying(artist="Us3", album="Cantaloop 2004", state="playing",
                     date=datetime.now())
    obj.save()


