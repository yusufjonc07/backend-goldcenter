from enum import Enum
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, root_validator, Field
from app.models.client import *


class FormClient(BaseModel):
    clientName: str
    chiefName: str
    inn: str
    phoneNumber: int
    extraPhoneNumber: Optional[int] = None

    @root_validator(pre=True)
    def check_phoneNumber_length(cls, values):
        errMsg = HTTPException(400, 'Telefon raqami noto`g`ri kiritildi!')

        if len(str(values.get('phoneNumber'))) != 9:
            raise errMsg
        if values.get('extraPhoneNumber') is not None and len(str(values.get('extraPhoneNumber'))) != 9:
            raise errMsg

        return values


class FormWarehouseClient(BaseModel):
    placeName: str = Field(..., max_length=10)
    placePrice: float = Field(..., gt=0)


class ConfirmFee(BaseModel):
    clientFeeId: int
    electrPrice: float = Field(..., ge=0)
    adPrice: float = Field(..., ge=0)
    electrAmount: float = Field(..., ge=0)
    value: float
