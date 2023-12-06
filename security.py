import logging

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from fastapi import Depends, Request, HTTPException
from models import UserModel

JWT_SECRET = "0b9d964a5e4d9bb2245f71d7c869236a939995ee5911c08ba7ae275dd6477e73"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/signin")
COOKIE_NAME = "Authorization"


def create_access_token(user):
    try:
        payload = {
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "active": user.is_active,
        }
        return jwt.encode(payload, key=JWT_SECRET, algorithm=ALGORITHM)
    except jwt.ExpiredSignatureError as ex:
        logger.error(f"Token creation failed: {str(ex)}")
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as ex:
        logger.error(f"Token creation failed: {str(ex)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def verify_token(token):
    try:
        payload = jwt.decode(token, key=JWT_SECRET)
        return payload
    except jwt.ExpiredSignatureError as ex:
        logger.error(f"Token verification failed: {str(ex)}")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError as ex:
        logger.error(f"Token verification failed: {str(ex)}")
        raise HTTPException(status_code=401, detail="Invalid token")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return user

def get_current_user_from_cookie(request: Request) -> UserModel:
    token = request.cookies.get(COOKIE_NAME)
    if token:
        user = verify_token(token)
        return user
