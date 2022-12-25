from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    email: list[EmailStr]


class VerifyCode(BaseModel):
    code: int


class TokenShow(BaseModel):
    token: str


class SearchEmail(BaseModel):
    email: str
