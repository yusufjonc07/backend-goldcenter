from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, APIRouter, HTTPException, status, WebSocketException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from databases.main import get_db, ActiveSession
from app.schemas.user import NewUser
from pydantic import BaseModel


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter(tags=["Xavsizlik"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    return user


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username=username, db=db)
    if not user:
        return False
    if not verify_password(password, user.passwordHash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# def get_current_ws_active_user(token: str, db: Session = ActiveSession):

#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     username: str = payload.get("sub")
#     if username:
#         token_data = TokenData(username=username)
#         user = get_user(username=token_data.username, db=db)

#         if user:
#             return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception

    return user


async def get_current_ws_user(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: NewUser = Depends(get_current_user)):
    if not current_user or current_user.disabled:
        raise HTTPException(status_code=401, detail="Bo`shatilgan hodim")
    return current_user


@auth_router.get("/me")
async def get_me(usr: NewUser = Depends(get_current_active_user)):
    usr.employee = usr.employee
    usr.employee.shift = usr.employee.shift
    return usr


@auth_router.post("/token", description="Bu joy login qilish uchun kerak boladi")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: User = authenticate_user(
        form_data.username, form_data.password, db=db)

    # if not form_data.client_secret:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="FSM Notification Token Mavjud Emas!",
    #     )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parolda xatolik!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user.deviceToken = form_data.client_secret
    db.commit()

    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "user": user}
