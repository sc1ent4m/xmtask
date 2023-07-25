from pydantic import BaseModel, UUID4
from typing import Dict


class Order(BaseModel):
    id: UUID4 | None = None
    stoks: str
    quantity: int
    status: str | None = None


class Orders(BaseModel):
    orders: Dict[str, Order]
