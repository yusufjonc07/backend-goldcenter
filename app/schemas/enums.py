from enum import Enum


class EmployeeRoles(str, Enum):
    director = "director"
    accountant = "accountant"
    headConstructor = "headConstructor"
    constructor = "constructor"
    guard = "guard"
    headGuard = "headGuard"
    headCleaner = "headCleaner"
    cleaner = "cleaner"
    clerk = "clerk"


class FloorTypes(str, Enum):
    rent = "rent"
    sold = "sold"


class MessageTypes(str, Enum):
    text = "text"
    image = "image"
    video = "video"
    audio = "audio"


messageTypeLabels = {
    "text": "matnli",
    "image": "rasmli",
    "video": "video",
    "audio": "ovozli"
}


class ChatTypes(str, Enum):
    headConstructor = "headConstructor"
    headGuard = "headGuard"
    headCleaner = "headCleaner"


class ExpenceTypes(str, Enum):
    none = "none"
    forFloor = "forFloor"
    forBranch = "forBranch"


class UserRoles(str, Enum):
    director = "director"
    accountant = "accountant"
    headConstructor = "headConstructor"
    headGuard = "headGuard"
    headCleaner = "headCleaner"
    clerk = "clerk"

class AgreementStatus(str, Enum):
    active = "active"
    paused = "paused"
    closed = "closed"

class AgreementType(str, Enum):
    rent = "rent"
    sold = "sold"

class MoneyHistoryTables(str, Enum):
    clientAgreement = "clientAgreement"

class MediaTypes(str, Enum):
    image="image"
    audio="audio"
    video="video"
    document="document" 

class ReportTypes(str, Enum):
    yearly="yearly"
    monthly="monthly"
    daily="daily"