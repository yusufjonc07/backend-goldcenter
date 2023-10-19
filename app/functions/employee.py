import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.employee import *
from app.models.user import User


def get_all_employees(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    employees = db.query(Employee).options(
        joinedload(Employee.shift)
    )

    # if search:
    # employees = employees.filter(
    # Employee.id.like(f"%{search}%"),
    # )

    all_data = employees.order_by(
        Employee.id.desc()).offset(offset).limit(limit)
    count_data = employees.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }
