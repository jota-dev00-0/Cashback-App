from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Float, DateTime
from datetime import datetime

from app.db.database import Base


class CashbackLog(Base):
    __tablename__ = "cashback_logs"

    id:             Mapped[int]      = mapped_column(primary_key=True, index=True)
    ip_address:     Mapped[str]      = mapped_column(String(45), nullable=False)
    client_type:    Mapped[str]      = mapped_column(String(20), nullable=False)
    purchase_value: Mapped[float]    = mapped_column(Float, nullable=False)
    cashback_base:  Mapped[float]    = mapped_column(Float, nullable=False)  # 5% (x2 se > R$500)
    cashback_bonus: Mapped[float]    = mapped_column(Float, nullable=False)  # +10% do base se VIP
    cashback_total: Mapped[float]    = mapped_column(Float, nullable=False)  # base + bonus
    created_at:     Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)