# -*- coding:utf-8 -*-
from ..routers import router
from ..utils.security import UserInfo, Token, OAuth2PasswordRequestForm
from ..utils.security import create_access_token, jwt_authenticate_user, token_is_true
from fastapi import Depends, HTTPException, status, Query
from typing import Optional
from datetime import timedelta
import config
import json


# 用户登录
@router.post('/api/auth/login/')
async def login(user_info: UserInfo):
    # print(user_info)
    # user = jwt_authenticate_user(db=config.fake_users_db, username=form_data.username, password=form_data.password)
    # if not user:
    #     raise HTTPException(
    #         status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    # 如果用户正确通过 则生成token
    # 设置过期时间
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_info.username}, expires_delta=access_token_expires
    )
    return {"code": 20000, "data": {"token": access_token, "token_type": "bearer"}}


# token验证
@router.get('/api/auth/info')
async def info(token: Optional[str]):
    # print('token', token)
    admin_data = {
        'roles': ['admin'],
        'introduction': 'I am a super administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Super Admin'
    }
    editor_data = {
        'roles': ['editor'],
        'introduction': 'I am an editor',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Normal Editor'
    }
    return {'code': 20000, 'data': admin_data}


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = jwt_authenticate_user(db=config.fake_users_db, username=form_data.username, password=form_data.password)
    if not user:
        return HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW -Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"code": 20000, "token": access_token}


# 用户登出
@router.post('/api/auth/logout')
async def logout():
    return {'code': 20000, 'data': 'success'}
