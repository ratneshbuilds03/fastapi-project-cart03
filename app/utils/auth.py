from datetime import datetime,timedelta
from app.config import settings
from jose import JWTError ,jwt 
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPTRE_MINUTES
    )
    to_encode.update({"exp": expire})
    secret_key = getattr(settings, "SECRET_KEY", getattr(settings, "SECRATE_KEY", ""))
    algorithm = getattr(settings, "ALGORITHM", getattr(settings, "ALGORITHAM", "HS256"))
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_token(token: str):
    try:
        secret_key = getattr(settings, "SECRET_KEY", getattr(settings, "SECRATE_KEY", ""))
        algorithm = getattr(settings, "ALGORITHM", getattr(settings, "ALGORITHAM", "HS256"))
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None