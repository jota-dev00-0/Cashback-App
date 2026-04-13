from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
 
from app.db.database import get_db
from app.models.schemas import CashbackRequest
from app.services import cashback_service
 
router = APIRouter(prefix="/api/v1", tags=["cashback"])
 
 
def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host
 
 
@router.post("/cashback")
def calculate_cashback(
    payload: CashbackRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    client_type = payload.client_type.lower()
 
    if client_type not in cashback_service.CLIENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo inválido. Use: {list(cashback_service.CLIENT_TYPES)}",
        )
 
    cashback_base, cashback_bonus, cashback_total = cashback_service.calculate_cashback(
        client_type, payload.purchase_value
    )
    ip = get_client_ip(request)
 
    cashback_service.save_log(
        db, ip, client_type, payload.purchase_value,
        cashback_base, cashback_bonus, cashback_total,
    )
 
    return {
        "client_type":    client_type,
        "purchase_value": payload.purchase_value,
        "cashback_base":  cashback_base,
        "cashback_bonus": cashback_bonus,
        "cashback_total": cashback_total,
    }
 
 
@router.get("/cashback/history")
def get_history(
    request: Request,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    ip   = get_client_ip(request)
    logs = cashback_service.get_history_by_ip(db, ip, limit)
 
    return [
        {
            "id":             log.id,
            "client_type":    log.client_type,
            "purchase_value": log.purchase_value,
            "cashback_base":  log.cashback_base,
            "cashback_bonus": log.cashback_bonus,
            "cashback_total": log.cashback_total,
            "created_at":     log.created_at,
        }
        for log in logs
    ]