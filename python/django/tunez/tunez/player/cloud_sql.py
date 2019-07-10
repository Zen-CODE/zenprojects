"""
This module houses code that interacts with the CloudSQL Postgress instance
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine


Base = declarative_base()


class NowPlaying(Base):
    """
    This class defines the model mapping the 'Now Playing' entries to the
    database table.
    """
    __tablename__ = 'now_playing'

    id = Column(Integer, primary_key=True)
    artist = Column(String)
    album = Column(String)
    state = Column(String)
    date = Column(Date)

    def __repr__(self):
        return "<NowPlaying(artist='{0}', album='{1}', state='{2}'".format(
            self.artist, self.album, self.state)


if __name__ == "__main__":
    from environs import Env
    env = Env()
    env.read_env()
    # engine = create_engine(env('SQLALCHEMY_DATABASE_URI'))
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    print("Database initialized")

