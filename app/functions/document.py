import math
from sqlalchemy.orm import Session
from app.models.document import *
from app.utils.fileUtil import file_size
from app.utils.pagination import pagination 


async def get_all_documents(search, page, limit, usr, db: Session):
    
    documents = db.query(Document)
   
    if search:
        # search filter here
        pass

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    queryPaginated = documents.offset(offset).limit(limit)
    count_data = documents.count()

    data_all = queryPaginated.all()

    data_res = []

    for data_one in data_all:
        
        data_res.append({
            'size': await file_size(data_one.fileName, 'documents')
        })

    return {
        "data": data_res,
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }

