import math
from sqlalchemy.orm import Session
from app.models.document import *
from app.utils.pagination import pagination 


def get_all_documents(search, page, limit, usr, db: Session):
    
    documents = db.query(Document)
   
    if search:
        # search filter here
        pass

    return pagination(documents, page, limit)

