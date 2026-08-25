from fastapi import APIRouter, Depends, HTTPException, status,Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_services import signup_user, login_user
from app.schemas.user import UserCreate, UserResponse, Token
from app.utils.rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def signup(user: UserCreate, request:Request, db: Session = Depends(get_db) ):
    new_user, error = signup_user(db, user)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return new_user

@router.post("/login", response_model=Token)
@limiter.limit("3/minute")
def login(
    request:Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token, error = login_user(db, form_data.username, form_data.password)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return {"access_token": token, "token_type": "bearer"}