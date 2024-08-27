from fastapi import APIRouter, Depends, status, HTTPException,Response
from sqlalchemy.orm import Session,joinedload
from .. import models, database, schemas
from ..hashing import Hash


router=APIRouter(
    prefix="/user",
    tags=['users']
)


get_db=database.get_db




@router.post("/",response_model=schemas.ShowUser,status_code=201)
def show_user_without_password(request:schemas.User, db:Session=Depends(get_db)):
    # hashedpassword=pwd_context.hash(request.password)
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=schemas.ShowUser)
def get_user(id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"user with this id {id} is not available")
    
    return user