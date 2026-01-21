from enum import Enum

from pydantic import BaseModel, EmailStr, constr


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Role = Role.USER


class UserCreate(UserBase):
    # Allow reasonably long passwords; pbkdf2_sha256 has no 72-byte limit
    password: constr(min_length=8, max_length=128)


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True
