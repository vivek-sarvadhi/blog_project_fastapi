from fastapi import FastAPI, Depends
from models import models
from core.database import engine
from routers import authentication
from schemas import authentication_schema
from core import ouath2

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(authentication.router)

@app.get('/')
def hello(get_current_user: authentication_schema.RegistrationBase = Depends(ouath2.get_current_user)):
    return {'hello': "world"}