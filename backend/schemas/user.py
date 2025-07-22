from pydantic import BaseModel, Field, EmailStr, ConfigDict
from uuid import UUID, uuid4

class CreateUser(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    email: EmailStr
    raw_password: str = Field(min_length=7, max_length=40)

class LoginUser(BaseModel):
    email: EmailStr
    raw_password: str = Field(min_length=7, max_length=40)


class ChangeUsernameUser(BaseModel):
    username: str = Field(min_length=2, max_length=30)

class ChangePasswordUser(BaseModel):
    old_raw_password: str = Field(min_length=7, max_length=40)
    new_raw_password: str = Field(min_length=7, max_length=40)

class ReadUser(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


