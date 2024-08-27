from sqlalchemy import Column ,Integer, String, ForeignKey
from .database import Base,engine
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "Blogs"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="user")
    

class User(Base):
    __tablename__ = "users"
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)
    user = relationship("Blog", back_populates="creator")
    