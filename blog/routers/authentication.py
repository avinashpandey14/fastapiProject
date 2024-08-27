
from fastapi import APIRouter, Depends, status, HTTPException,Response
from sqlalchemy.orm import Session,joinedload
from .. import models, database, schemas,token
from ..hashing import Hash
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter(
    tags=['Login']
)

@router.post("/login")
def create_login(request:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"username not found with this {request.username}")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Password Incorrect ")
    access_token_expires = timedelta(minutes=15)
    access_token = token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")