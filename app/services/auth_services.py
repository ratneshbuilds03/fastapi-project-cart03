from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.auth import hash_password ,verify_password,create_access_token

def signup_user(db:Session,user_data:UserCreate):
    existing = db.query(User).filter(User.email ==user_data.email).first()
    if existing :
        return None,"Email already registered"
    
    new_user = User(
        name = user_data.name,
        email =user_data.email,
        password_hash = hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user , None
def login_user(db:Session,email:str ,password:str):
    user =db.query(User).filter(User.email==email).first()
    if not user or not verify_password(password,user.password_hash):
        return None ,"Invalid email or password"
    token = create_access_token({"sub":str(user.id)})
    return token ,None