from datetime import date
import uuid
from fastapi import Body, File, HTTPException, APIRouter, Depends, UploadFile
from typing import Optional
from app.models.clientAgreement import ClientAgreement
from app.models.employee import Employee
from app.models.expense import Expense
from app.models.user import User
from app.schemas.enums import ExpenceTypes, ExpenseTables, IncomeTables, MoneyHistoryTables
from app.schemas.user import NewUser
from app.utils.fileUtil import save_file, validate_file
from app.utils.handler import integrityHandler
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.functions.moneyHistory import *

moneyHistory_router = APIRouter(tags=['Moneyhistory Endpoint'])


    
# @moneyHistory_router.post("/expense/create")
# async def create_new_expense(
#     ownerTable: ExpenseTables = Body(...),
#     ownerId: int = Body(...),
#     value: float = Body(...),
#     moneyFormId: int =  Body(...),
#     comment: str =  Body(..., min_length=5),
#     fileName: Optional[UploadFile] = File(...),
#     db: Session = ActiveSession,
#     usr: User = Depends(get_current_active_user)
# ):
    

#     if not usr.userRole in ['any_role']:
#         try:

#             if fileName != 'none':
#                 _fileName = await validate_file(fileName, ['document', 'image'], 3)
#             else:
#                 _fileName = None
            
#             if ownerTable in ['clientAgreement',] and value <= 0:
#                 raise HTTPException(400, "Olinayotgan pul miqdori noto'g'ri")
            
#             isProceed = False
#             floorId = 0
#             branchId = usr.branchId
#             addingtofee = 'none'
            
#             # if ownerTable=='clientAgreement':
                
#             #     clientAgreement = db.get(ClientAgreement, ownerId)
#             #     if not clientAgreement: 
#             #         raise HTTPException(400, "Mijoz shartnomasi topilmadi")
#             #     else:
#             #         # raise HTTPException(400, f"{type(clientAgreement.balance).__name__} {type(value).__name__}")
#             #         clientAgreement.balance += value 
#             #         try:
#             #             db.commit()
#             #             isProceed = True
#             #             floorId = clientAgreement.shop.floorId
#             #             branchId = clientAgreement.shop.floor.branchId
#             #         except Exception as e:
#             #             integrityHandler(e)
#             # else:
#             #     isProceed = True

#             isProceed = True
               

#             if isProceed:
#                 new_moneyHistory = MoneyHistory(
#                     ownerTable=ownerTable,
#                     ownerId=ownerId,
#                     value=value,
#                     moneyFormId=moneyFormId,
#                     floorId=floorId,
#                     comment=comment,
#                     branchId=branchId,
#                     userId=usr.id,
#                     fileName=_fileName,
#                     addingToFee=addingtofee
#                 )

#             db.add(new_moneyHistory)
#             db.commit()

#             if _fileName:
#                 await save_file(fileName, _fileName, f"moneyHistories/{date.year}/{date.month}/{date.day}")

#             raise HTTPException(200, "Ma`lumotlar saqlandi!")
#         except IntegrityError as e:
#             raise HTTPException(400, e.args)
#     else:
#         raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


# @moneyHistory_router.put("/moneyHistory/{id}/update")
# async def update_one_moneyHistory(
#     id: int,
#     liablePerson: str = Body(..., min_length=5),
#     shopId: int = Body(...),
#     clientId: str = Body(...),
#     monthlyFee: float = Body(..., ge=0),
#     balance: float = Body(...),
#     status: AgreementStatus = Body(...),
#     type: AgreementType = Body(...),
#     startedAt: date = Body(...),
#     agreementFile: Optional[UploadFile] = File(None),
#     db: Session = ActiveSession,
#     usr: User = Depends(get_current_active_user)
# ):
#     if not usr.userRole in ['any_role']:
#         try:
#             moneyHistory = db.query(ClientAgreement).filter(ClientAgreement.id == id)
#             this_moneyHistory = moneyHistory.first()
#             if this_moneyHistory:

#                 old_file_path = f"assets/moneyHistorys/{this_moneyHistory.agreementFile}"

#                 if agreementFile:

#                     if not agreementFile.content_type in CONTENT_TYPE_LOOKUP_TABLE:
#                         raise HTTPException(
#                             400, "Fayl formati pdf, docx, xls yoki xlsx bo`lishi kerak!")

#                     file_contents = await agreementFile.read()

#                     filename = f"{uuid.uuid4()}__{agreementFile.filename}"
#                     if len(file_contents) > 3000000:
#                         raise HTTPException(
#                             400, "Fayl kattaligi maksimal 3 MB!")
#                 else:
#                     filename = this_moneyHistory.agreementFile
#                     file_contents = None

#                 moneyHistory.update({
#                     ClientAgreement.fileName: filename,
#                     ClientAgreement.shopId: shopId,
#                     ClientAgreement.clientId: clientId,
#                     ClientAgreement.monthlyFee: monthlyFee,
#                     ClientAgreement.balance: balance,
#                     ClientAgreement.status: status,
#                     ClientAgreement.type: type,
#                     ClientAgreement.startedAt: startedAt,
#                     ClientAgreement.liablePerson: liablePerson,
#                 })
#                 db.commit()

#                 if file_contents:
#                     with open(f"assets/moneyHistoryAgreements/{filename}", "wb") as f:
#                         f.write(file_contents)

#                         if exists(old_file_path):
#                             os.unlink(old_file_path)

#                 raise HTTPException(
#                     status_code=200, detail="O`zgarish saqlandi!")
#             else:
#                 raise HTTPException(
#                     status_code=400, detail="So`rovda xatolik!")
#         except IntegrityError as e:
#             integrityHandler(e)
#     else:
#         raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
