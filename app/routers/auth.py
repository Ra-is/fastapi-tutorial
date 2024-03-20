from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import engine,  get_db
from ..utils import hash,verify
from ..schemas import  UserLogin, Token
from ..oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login', response_model=Token)
def get_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid User")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid User")
    else:
        # create token
        access_token = create_access_token(data={"user_id" : user.id})
        return {"access_token": access_token, "token_type": "bearer"}
