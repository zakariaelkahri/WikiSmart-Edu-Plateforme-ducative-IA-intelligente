from pydantic import BaseModel

from app.schemas.user import Role, UserRead


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None
    role: Role | None = None


class AuthenticatedUser(BaseModel):
    user: UserRead
    token: Token

