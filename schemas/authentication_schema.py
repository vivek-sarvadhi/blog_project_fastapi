from pydantic import BaseModel
from typing import Optional


class RegistrationBase(BaseModel):
    email: str = None
    password: str = None


class TokenData(BaseModel):
    email: Optional[str] = None

