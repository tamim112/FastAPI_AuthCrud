from lib.library import *
from . import models
from config.db import engine ,Base, SessionLocal


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency=Annotated[Session, Depends(get_db)]


#Database Model
class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True,index=True)
    name= Column(String(100), unique=True)
    username= Column(String(100), unique=True)
    password= Column(String(100))
    email= Column(String(50))
    mobile= Column(String(50))
    age= Column(Integer)
    
class Post(Base):
    __tablename__='posts'
    id = Column(Integer, primary_key=True,index=True)
    title= Column(String(100))
    content= Column(String(200))
    user_id= Column(String(50))


#Base Model
models.Base.metadata.create_all(bind=engine)
class UserBase(BaseModel):
    name:str
    username:str
    password:str
    email:str
    mobile:str
    age:int

class PostBase(BaseModel):
    title:str
    content:str
    user_id:int
    
