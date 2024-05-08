from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.config import configurations

# def get_session_maker():
db_engine = create_engine(
    configurations.DATABASE_URI.unicode_string(), pool_pre_ping=True
)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
# The sessionmaker factory generates new Session objects
# when called, creating them given the configurational arguments established here.


@contextmanager
def get_db():
    session = session_maker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        # can roll other things back here
        raise
    finally:
        session.close()
