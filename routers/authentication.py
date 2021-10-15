from fastapi import APIRouter, Depends, status, Form,HTTPException
from schemas import authentication_schema
from models import models
from sqlalchemy.orm import Session
from core import database
from core.hashing import Hash
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from core import jwttoken


router = APIRouter()


@router.post('/registration', status_code=status.HTTP_201_CREATED)
def Registration(email: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    email1 = db.query(models.User).filter(models.User.email == email).first()
    if email1:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'status': status.HTTP_400_BAD_REQUEST, 'error':True, 'error_message':"email already use please try another email"})
    new_user = models.User(email=email, password=Hash.get_password_hash(password))
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response_object = {
        "email": email,
    }
    return JSONResponse(content={'status': status.HTTP_201_CREATED,
                                    'error': False,
                                    "message":"User Register Successfully",
                                    "result":response_object
                                    },status_code=status.HTTP_201_CREATED)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:    
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'status': status.HTTP_400_BAD_REQUEST, 'error':True, 'error_message':"Invalid credential"})
    if not Hash.verify_password(user.password, request.password):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'status': status.HTTP_400_BAD_REQUEST, 'error':True, 'error_message':"Invalid password"})
    access_token = jwttoken.create_access_token(data={"sub": request.username})
    return JSONResponse(content={"Status": status.HTTP_200_OK,
                                "error": False,
                                "message": "User Login Successfully.",
                                 "results": {'id': user.id,
                                            'email': user.email,
                                            'token': access_token,}},
                                status_code=status.HTTP_200_OK)