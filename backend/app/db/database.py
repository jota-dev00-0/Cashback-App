from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "Variável DATABASE_URL não encontrada. "
        "Crie o arquivo backend/.env com: DATABASE_URL=postgresql://..."
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,    # testa a conexão antes de usar — descarta conexões mortas
    pool_recycle=300,      # recria conexões do pool a cada 5 min (evita timeout do Supabase free tier)
    connect_args={
        "connect_timeout": 10,  # desiste de conectar após 10s em vez de travar indefinidamente
    },
)


class Base(DeclarativeBase):
    pass


Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()