from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import config



Base = declarative_base()

# Create the engine with the database URL from config
engine = create_engine(config.SQLALCHEMY_DATABASE_URL)

# Create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    from app.models import User  # Local import to avoid circular dependency
    Base.metadata.create_all(bind=engine)


create_tables()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()