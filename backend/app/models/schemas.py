from pydantic import BaseModel, Field


class CashbackRequest(BaseModel):
    client_type:    str   = Field(..., description="standard | vip")
    purchase_value: float = Field(..., gt=0, description="Valor da compra em R$")