from pydantic import BaseModel
from typing import List, Optional

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    email: str

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    creator: ShowUser

    class Config():
        orm_mode = True