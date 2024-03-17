from enum import Enum

ROLES = [
    "director",
    "accountant",
    'headConstructor',
    'constructor',
    'guard',
    'headGuard',
    'headCleaner',
    'cleaner',
    'marketing',
    'clerk',
]

ROLE_LABELS = {
    "director": "Direktor",
    "accountant": 'Buxgalter',
    'headConstructor': 'Xo`z bo`limi boshlig`i',
    'constructor': 'Xo`z bo`limi hodimi',
    'guard': 'Qorovul',
    'headGuard': 'Xavfsizlik bo`limi boshlig`i',
    'headCleaner': 'Tozalik bo`limi boshlig`i',
    'cleaner': 'Tozalik bo`limi hodimi',
    'marketing': 'Marketing bo`limi hodimi',
    'clerk': 'Pattachi',
}

DEPARTMENT_LABELS = {
    "director": "Boshqaruv",
    "accountant": 'Buxgalteriya',
    'headConstructor': 'Xo\'jalik',
    'constructor': 'Xo\'jalik',
    'guard': 'Qorovul',
    'headGuard': 'Xavfsizlik',
    'headCleaner': 'Tozalik',
    'cleaner': 'Tozalik',
    'marketing': 'Marketing',
    'clerk': 'Buxgalteriya',
}


class EmployeeRoles(str, Enum):
    director = "director"
    accountant = "accountant"
    headConstructor = "headConstructor"
    constructor = "constructor"
    guard = "guard"
    headGuard = "headGuard"
    headCleaner = "headCleaner"
    cleaner = "cleaner"
    marketing = "marketing"
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


class TaskTypes(str, Enum):
    negative = "negative"
    positive = "positive"


class NotificationTypes(str, Enum):
    task = "task"
    document = "document"


class ExpenceTypes(str, Enum):
    salary = "salary"
    regular = "regular"
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


class IncomeType(str, Enum):
    rent = "rent"
    utility = "utility"
    infrastructure = "infrastructure"
    regular = "regular"
    other = "other"


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
    image = "image"
    audio = "audio"
    video = "video"
    document = "document"


class ReportTypes(str, Enum):
    monthly = "monthly"
    daily = "daily"
