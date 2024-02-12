from lib.library import *

#File path
from controller.user import user
from controller.post import post
from config.auth import router as auth_router

from config.auth import user_dependancy
from config.models import db_dependency

app=FastAPI()

app.include_router(auth_router)
app.include_router(user)
app.include_router(post)


@app.get('/',status_code=status.HTTP_200_OK)
def index(user:user_dependancy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authorization Failed')
    return {"Nice":"OK"}

