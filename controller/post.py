
from lib.library import *
from config.models import Post
#for authentication
from config.models import db_dependency
from config.auth import user_dependancy

post=APIRouter()

###################### View list Start ###########################

@post.get('/read_post')
def get_post(user:user_dependancy,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authorization Failed')
    
    #model based
    # users = db.query(models.User.id, models.User.name).all()
    # result = [{"id": user.id, "name": user.name} for user in users]
    
    #Raw model
    raw_query = text("SELECT u.id, u.name, p.title,p.content FROM users u,posts p where u.id=p.user_id")
    posts = db.execute(raw_query)
    
    result=[]
    for post in posts:
        result.append({"title": post.title,"content": post.content,'User':post.name})

    return result
###################### View list End ###########################


###################### INSERT Start ###########################
#Raw Model specific field
@post.post('/create_post')
def create_user(user:user_dependancy,db:db_dependency,title:str,content:str,user_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authorization Failed')
    
    new_post = Post(title=title,content=content,user_id=user_id)
    db.add(new_post)
    db.commit()
    res_data={
        'status':'200',
        'ret_str':'Post Successfully Inserted'
    }
    return res_data

###################### INSERT End ###########################
