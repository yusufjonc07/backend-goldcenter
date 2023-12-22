from enum import Enum
from typing import Optional
from pydantic import BaseModel
from app.models.shop import *


class NewShop(BaseModel):
    name: str
    number: str
    floorId: int
    area: float
    fromTop: float
    fromLeft: float
    boxWith: float
    boxHeight: float


class DivideShop(BaseModel):
    shopId: int
    areaA: float
    areaB: float


class CombineShops(BaseModel):
    mainShopId: int
    deletingShopId: int
    number: str
    area: float
    fromTop: float
    fromLeft: float
    boxWith: float
    boxHeight: float


class UpdateShop(BaseModel):
    name: str
    number: str
    floorId: int
    area: float
    fromTop: float
    fromLeft: float
    boxWith: float
    boxHeight: float
