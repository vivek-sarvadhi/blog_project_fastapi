from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, status, security
from sqlalchemy.orm import Session
from core import jwttoken, database
from jose import JWTError, jwt
from models import models
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     print("yessss")
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return jwttoken.verify_token(token, credentials_exception)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    print("token", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload",payload)
        email = payload.get("sub")
        print("email",email)
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # user = models.User.get(email=email)
    user = db.query(models.User).filter_by(email=email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user
