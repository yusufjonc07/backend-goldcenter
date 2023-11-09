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



messageTypeLabels = {
    "text": "matnli",
    "image": "rasmli",
    "video": "video",
    "audio": "ovozli"
}


class ChatTypes(str, Enum):
    headCleaner = "headCleaner"
    headConstructor = "headConstructor"
    headGuard = "headGuard"
    accountant = "accountant"

class MessageTypes(str, Enum):
    request = "request"
    negative = "negative"
    positive = "positive"


class ExpenceTypes(str, Enum):
    salary = "salary"
    construction = "construction"
    other = "other"

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

class IncomeTables(str, Enum):
    clientAgreement = "clientAgreement"

class MoneyHistoryTables(str, Enum):
    income = "income"
    expense = "expense"
    clientAgreement = "clientAgreement"
    employee = "employee"

class ExpenseTables(str, Enum):
    employee = "employee"

class MediaTypes(str, Enum):
    image="image"
    audio="audio"
    video="video"
    document="document" 

class ReportTypes(str, Enum):
    monthly="monthly"
    daily="daily"