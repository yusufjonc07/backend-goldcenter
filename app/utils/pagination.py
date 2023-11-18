from sqlalchemy.orm import Session
import math

def pagination(query: Session, page: int, limit: int):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    queryPaginated = query.offset(offset).limit(limit)
    count_data = query.count()

    return {
        "data": queryPaginated.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }