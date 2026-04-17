from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base
from app.utils.constants import DB_PATH, DB_URL

DATABASE_DIR = Path(DB_PATH).parent
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
