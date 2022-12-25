from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from mychat.src.schemas import users_sc
from mychat.src.crud import users_crud
from mychat.src.controller import email_sender
from mychat.src.controller.code_generate import CodeGenerator
from mychat.src.controller.token_generator import TokenGenrator
from mychat.src.db.database import mongo_client


router = APIRouter(tags=["user"], prefix="/user")

code_generator = CodeGenerator()
user_access = TokenGenrator()


@router.post("/send-email")
async def create_user(email: users_sc.EmailSchema, background_task: BackgroundTasks):
    verify_code = code_generator.generator()
    query = users_crud.get_otp_code(verify_code)
    if query:
        raise HTTPException(detail='otp code alredy exist', status_code=400)
    email_sender.send_email_verify(
        background_task=background_task, emails=email, verify_code=verify_code)
    users_crud.set_otp_code(code=verify_code)
    return {'status': 'success'}


@router.post('/verify-code', response_model=users_sc.TokenShow)
async def verify_code(email: users_sc.EmailSchema, code: users_sc.VerifyCode):
    code_query = users_crud.get_otp_code(code=code.code)
    if not code_query:
        raise HTTPException(detail='Code does not exist', status_code=404)
    if not code_query['is_valid']:
        raise HTTPException(detail='Code Not valid', status_code=400)
    if not datetime.now() < code_query['datetime'] + timedelta(minutes=5):
        users_crud.update_otp_code(code=code.code)
        raise HTTPException(detail='code time is expire', status_code=403)
    user = users_crud.create_user(email=email.dict().get('email')[0])
    token = user_access.create_token(email=user['email'], user_id=user['id'])
    users_crud.update_otp_code(code=code.code)
    return {'token': token}


@router.post('/get-user')
async def get_users(user: dict = Depends(user_access.current_user)):
    return user


@router.post('/search-user')
async def search_user(email: users_sc.SearchEmail):
    if email.email is '':
        return []
    return users_crud.search_user(email=email.email)
