from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL tidak ditemukan di .env")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping  = True,
    pool_size      = 10,
    max_overflow   = 20,
    pool_recycle   = 3600,
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush  = False,
    bind       = engine
)

Base = declarative_base()


def get_db():
    """
    Dependency injection untuk semua router.
    Pakai dengan: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    """Cek koneksi database saat startup"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"❌ DB Error: {e}")
        return False