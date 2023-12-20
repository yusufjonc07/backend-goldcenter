from enum import Enum
from pydantic import BaseModel
from typing import Optional, List


class NewAttandance(BaseModel):
    user_id: int
    plant_id: Optional[int] = 0


class AttTypeHik(str, Enum):
    checkIn = "checkIn"
    checkOut = "checkOut"


class UpdateAttandance(BaseModel):
    type: str
    user_id: int
    wage: float
    authorizator: str
    datetime: str


class AccessControllerEvent(BaseModel):
    deviceName: str
    name: str
    employeeNoString: str
    attendanceStatus: AttTypeHik


class EventLogItem(BaseModel):
    dateTime: str
    deviceID: str
    AccessControllerEvent: AccessControllerEvent


class EventLog(BaseModel):
    event_log: List[EventLogItem]
