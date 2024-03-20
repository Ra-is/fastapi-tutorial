from jose import JOSEError, jwt 
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

outh2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRATION_MIN = settings.access_token_expire_minutes

def create_access_token(data: dict):
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MIN)
    expire_timestamp = expire.timestamp()
    to_encode.update({"exp": expire_timestamp})
    
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_access_token(token: str, credential_exception):

    try:
        paylod = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = paylod.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except JOSEError as error:
        raise credential_exception
    return token_data

def get_current_user(token: str = Depends(outh2_schema), db:Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials")
    
    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
