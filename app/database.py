from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = 'sqlite:///autopick.db'
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

@event.listens_for(Engine, "connect")
def enable_foreign_keys(connection,record):
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()