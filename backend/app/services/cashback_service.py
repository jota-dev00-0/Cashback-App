from sqlalchemy.orm import Session
from app.models.cashback_log import CashbackLog

BASE_PERCENT     = 5.0   # cashback base para todos os clientes
VIP_BONUS_FACTOR = 0.10  # bônus VIP: 10% sobre o cashback base calculado
DOUBLE_THRESHOLD = 500.0 # compras acima deste valor dobram o cashback base

CLIENT_TYPES = ("standard", "vip")


def calculate_cashback(client_type: str, purchase_value: float) -> tuple[float, float, float]:
    """
    Regras (em ordem de aplicação):
      1. Cashback base = 5% sobre o valor da compra
      2. Se purchase_value > 500, o cashback base é dobrado (vale para todos)
      3. Se VIP, soma 10% sobre o cashback base já calculado
    Retorna (cashback_base, cashback_bonus, cashback_total).
    """
    # 1. Base
    cashback_base = round(purchase_value * BASE_PERCENT / 100, 2)

    # 2. Dobro para compras acima de R$ 500
    if purchase_value > DOUBLE_THRESHOLD:
        cashback_base = round(cashback_base * 2, 2)

    # 3. Bônus VIP
    cashback_bonus = round(cashback_base * VIP_BONUS_FACTOR, 2) if client_type == "vip" else 0.0

    cashback_total = round(cashback_base + cashback_bonus, 2)
    return cashback_base, cashback_bonus, cashback_total


def save_log(
    db: Session,
    ip: str,
    client_type: str,
    purchase_value: float,
    cashback_base: float,
    cashback_bonus: float,
    cashback_total: float,
) -> CashbackLog:
    log = CashbackLog(
        ip_address=ip,
        client_type=client_type,
        purchase_value=purchase_value,
        cashback_base=cashback_base,
        cashback_bonus=cashback_bonus,
        cashback_total=cashback_total,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_history_by_ip(db: Session, ip: str, limit: int = 50) -> list[CashbackLog]:
    return (
        db.query(CashbackLog)
        .filter(CashbackLog.ip_address == ip)
        .order_by(CashbackLog.created_at.desc())
        .limit(limit)
        .all()
    )