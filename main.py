from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app=FastAPI()

@app.get("/")
def index():
    return {'data':{'name':'blog'}}


# QUERY Paramater
@app.get("/blog")
def query(limit,published:bool):
    if published:
        return {'data': f'{limit} published blogs from db'}
    else:
        return {'data': f'{limit} blogs from db'}

##Query parameter using sort
@app.get("/blog")
def query(limit=10,published:bool=True, sort:Optional[str]=None):
    if published:
        return {'data': f'{limit} published blogs from db'}
    else:
        return {'data': f'{limit} blogs from db'}
#####


@app.get("/blog/unpublished")
def unpublished():
    #fetch the ID details of id
    return {'data': "all unpublished blogs"}

@app.get("/blog/{id}")
def show(id : int):
    #fetch the ID details of id
    return {'data': id}

@app.get("/blog/{id}/comments")
def comments(id):
    #fetch comments of ID id
    return {'data': {'1','2'}}

#POST Methods

class Blog(BaseModel):
    title:str
    body:str
    published:Optional[bool]
    
@app.post("/blog")
def create_blog(blog:Blog):   # we can use any name instead of request 
    # return {'data': f"Blog is created with title as {request.title}"}
    return {'data': f"Blog is created with title as {blog.title}"}




# if want to run on your sevrer url and port then
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8100)



     


@app.post("/blog",status_code=201,tags=['blogs'])
def create_blog(request:schemas.Blog, db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog",tags=['blogs'])
def all(db:Session=Depends(get_db)):
    all_blogs=db.query(models.Blog).all()
    return all_blogs

@app.get("/blog/{id}",response_model=schemas.ShowBlog,status_code=200,tags=['blogs'])
def particular_blog_with_id(id,response:Response,db:Session=Depends(get_db)):
    blog_with_id=db.query(models.Blog).options(joinedload(models.Blog.creator)).filter(models.Blog.id==id).first()
    if not blog_with_id:
        raise HTTPException(status_code=404, detail=f"blog with this id {id} is not available")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f"blog with this id {id} is not available"}
    if not blog_with_id.creator:
        blog_with_id.creator = None
    return blog_with_id


@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def destroy(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).delete()
    db.commit()
    return blog

@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update_blog(id,request:schemas.Blog, db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"blog with this id {id} is not available")
    blog.update(request.dict())
    db.commit()
    return "updated"



# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/user/",status_code=201,tags=['users'])
def create_user(request:schemas.User, db:Session=Depends(get_db)):
    # hashedpassword=pwd_context.hash(request.password)
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/user/",response_model=schemas.ShowUser,status_code=201,tags=['users'])
def show_user_without_password(request:schemas.User, db:Session=Depends(get_db)):
    # hashedpassword=pwd_context.hash(request.password)
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}",response_model=schemas.ShowUser,tags=['users'])
def get_user(id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"user with this id {id} is not available")
    
    return user
