import math
from sqlalchemy.orm import joinedload, Session
from app.models.employee import *
from app.utils.pagination import pagination



def get_all_employees(search, roles, page, limit, usr, db: Session):

    employees = db.query(Employee).options(
        joinedload(Employee.shift)
    )

    if len(roles) > 0:
        employees = employees.filter(Employee.role.in_(roles.split(';')))
    
    #if search:
        #employees = employees.filter(
            #Employee.id.like(f"%{search}%"),
        #)

    return pagination(employees, page, limit)