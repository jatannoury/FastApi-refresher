from datetime import timedelta,datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from database import session_local
from models import Users
from passlib.context import CryptContext
from jose import jwt

router = APIRouter()
SECRET_KEY = 'afcc2dec-da61-44fd-940f-3f595b9bca11'
ALGORITHM = 'HS256'


bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role:str

class Token(BaseModel):
    access_token:str
    token_type:str
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session,Depends(get_db)]

def authenticate_user(username:str, password:str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    print(user)
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user
def create_access_token(username:str,user_id:int,expires_delta:timedelta):
    encode = {
        "sub":username,
        "id":user_id
    }
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username= create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )

    db.add(create_user_model)
    db.commit()

@router.post("/token",response_model=Token)
async def login_for_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user = authenticate_user(username=form_data.username,password=form_data.password,db=db)
    if not user:
        return "Failed Auth"
    token = create_access_token(username=user.username,user_id=user.id,expires_delta=timedelta(minutes=20))
    return {"access_token":token,"token_type":"Bearer"}
