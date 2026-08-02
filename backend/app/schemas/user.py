from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)

    email: EmailStr

    password: str = Field(min_length=8, max_length=128)

    country: str

    education_level: str


class UserResponse(BaseModel):
    id: int

    full_name: str

    email: EmailStr

    country: str

    education_level: str

    xp: int

    level: int

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str