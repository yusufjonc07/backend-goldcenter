from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

UNIQUE_CONSTRAINT_VIOLATION_CODE = 1062
FOREIGN_KEY_CONSTRAINT_VIOLATION_CODE = 1452

def integrityHandler(errorException: IntegrityError):
    
    errorCode = errorException.orig.args[0]

    if errorCode == UNIQUE_CONSTRAINT_VIOLATION_CODE:
        raise HTTPException(400, 'Kiritilgan ma`lumot bazada mavjud!')
    
    if errorCode == FOREIGN_KEY_CONSTRAINT_VIOLATION_CODE:
        raise HTTPException(400, 'Kiritilgan ma`lumot bazada mavjud emas!')

    raise HTTPException(400, 'Ma`lumotlarni qayta ishlashda xatolik!')