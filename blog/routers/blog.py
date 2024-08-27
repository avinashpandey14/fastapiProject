from typing import List
from fastapi import APIRouter, Depends, status, HTTPException,Response
from sqlalchemy.orm import Session,joinedload
from .. import models, database, schemas, oauth
from ..hashing import Hash


router=APIRouter(
    prefix="/blog",
    tags=['Blogs'],
)


get_db=database.get_db

@router.get("/",response_model=List[schemas.ShowBlog])
def all(db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth.get_current_user)):
    all_blogs=db.query(models.Blog).all()
    return all_blogs

# @router.get("/",response_model=List[schemas.ShowBlog])
# def all(db:Session=Depends(get_db)):
#     all_blogs=db.query(models.Blog).all()
#     return all_blogs

@router.post("/",status_code=201)
def create_blog(request:schemas.Blog, db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth.get_current_user)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/{id}",response_model=schemas.ShowBlog,status_code=200)
def particular_blog_with_id(id,response:Response,db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth.get_current_user)):
    blog_with_id=db.query(models.Blog).options(joinedload(models.Blog.creator)).filter(models.Blog.id==id).first()
    if not blog_with_id:
        raise HTTPException(status_code=404, detail=f"blog with this id {id} is not available")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f"blog with this id {id} is not available"}
    if not blog_with_id.creator:
        blog_with_id.creator = None
    return blog_with_id


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth.get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).delete()
    db.commit()
    return blog

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request:schemas.Blog, db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth.get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"blog with this id {id} is not available")
    blog.update(request.dict())
    db.commit()
    return "updated"
