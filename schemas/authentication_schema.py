from pydantic import BaseModel, EmailStr
from typing import Optional


class RegistrationBase(BaseModel):
    email: EmailStr
    password: str = None


class TokenData(BaseModel):
    email: Optional[str] = None

