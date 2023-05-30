from schemas import blog_schema
from models import models
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter, Form, HTTPException, Response
from core import database, ouath2, jwttoken
from fastapi.responses import JSONResponse
from typing import Optional, List
from fastapi_pagination import Page, add_pagination, paginate


router = APIRouter()


@router.post('/blogcreate', status_code=status.HTTP_201_CREATED)
def create(title: str = Form(...), body: str = Form(...), db: Session = Depends(database.get_db), current_user: models.User = Depends(ouath2.get_current_user)):
    new_blog = models.Blog(title=title, body=body, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    response_object = {
        "id": new_blog.id,
        "title": new_blog.title,
        "body": new_blog.body,
        "user": new_blog.user_id,
    }
    return JSONResponse(content={'status': status.HTTP_201_CREATED,
                                    'error': False,
                                    "message":"blog created Successfully",
                                    "result":response_object
                                    },status_code=status.HTTP_201_CREATED)



@router.get('/blog', response_model=Page[blog_schema.ShowBlog])
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return paginate(blogs)

add_pagination(router)


@router.get('/blog_user', response_model=Page[blog_schema.ShowBlog])
def all(db: Session = Depends(database.get_db), current_user: models.User = Depends(ouath2.get_current_user)):
    blogs = db.query(models.Blog).filter_by(user_id=current_user.id).all()
    return paginate(blogs)
add_pagination(router)


@router.get('/blog/{id}', status_code=200, response_model=blog_schema.ShowBlog)
def show(id:int , response: Response, db: Session = Depends(database.get_db), current_user: models.User = Depends(ouath2.get_current_user)):
    blog = db.query(models.Blog).filter_by(id = id, user_id=current_user.id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    return blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destory(id:int , db: Session = Depends(database.get_db), current_user: models.User = Depends(ouath2.get_current_user)):
    blog = db.query(models.Blog).filter_by(id = id, user_id=current_user.id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(content={'status': status.HTTP_200_OK,
                                    'error': False,
                                    "message":"blog delete Successfully",
                                    # "result":response_object
                                    },status_code=status.HTTP_200_OK)


@router.put('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update(id:int, request: blog_schema.Blog, db: Session = Depends(database.get_db), current_user: models.User = Depends(ouath2.get_current_user)):
    blog = db.query(models.Blog).filter_by(id= id, user_id=current_user.id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    # blog.update(request)
    blog.update({'title':request.title, 'body':request.body})
    db.commit()
    response_object = {
        # "id": blog.id,
        "title": request.title,
        "body": request.body,
        # "user": blog.user_id,
    }
    return JSONResponse(content={'status': status.HTTP_200_OK,
                                    'error': False,
                                    "message":"blog updated Successfully",
                                    "result":response_object
                                    },status_code=status.HTTP_200_OK)