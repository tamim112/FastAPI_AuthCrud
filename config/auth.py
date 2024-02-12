from lib.library import *
from config.models import User
from config.models import db_dependency

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'],  deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class Token(BaseModel):
    access_token:str
    token_type:str



@router.post("/token",response_model=Token)
async def login_for_access_data(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    
    user=authenticate_user(form_data.username, form_data.password,db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
    token=create_access_token(user.username,user.id,timedelta(minutes=20))
    return {"access_token":token, "token_type":"bearer"}
    
def authenticate_user(username:str,password:str,db):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.password):
        return False
    return user

def create_access_token(username:str,user_id:int,expires_delta:timedelta):
    encode={'sub':username,'id':user_id}
    expires=datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username:str=payload.get('sub')
        user_id:int=payload.get('id')
        if username is None and user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
        return {'username':username,'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')

user_dependancy=Annotated[dict,Depends(get_current_user)]
