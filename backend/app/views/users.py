# -*- coding:utf-8 -*-
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import UserInfo, Token
from utils.security import create_access_token, jwt_authenticate_user
from utils.decorators import login_require
from db.set_db import create_session
from db.set_redis import r, pool
from models.users import User
from starlette.requests import Request
from typing import Optional
from datetime import timedelta
import config

user_router = APIRouter()


# 用户登录
@user_router.post('/login', summary='用户登录')
async def login(user_info: UserInfo):
    user = jwt_authenticate_user(User, user_info.username, user_info.password)
    if user:
        # 如果用户正确通过 则生成token
        # 设置过期时间
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={'sub': user_info.username}, expires_delta=access_token_expires
        )
        user_name = user.get('username')
        # redis存储用户的tokern信息
        r.set(access_token, user_name, ex=config.REDIS_EXPIRE_TIME)
        return {'code': 200, 'data': {'access_token': access_token, 'token_type': 'bearer'}}
    else:
        raise HTTPException(
            status_code=401,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )


# token验证
@user_router.get('/info', summary='获取用户信息')
@login_require
async def info(request: Request, token: Optional[str]):
    print('token', token)
    # 判断token是否过期
    if r.get(token):
        username = r.get(token)
        session = create_session()
        user_query = session.query(User).filter_by(username=username).first()
        user_dict = {'username': user_query.username,
                     'email': user_query.email,
                     'roles': [user_query.roles],
                     'introduction': user_query.introduction,
                     'avatar': user_query.avatar}
        session.close()

        return {'code': 200, 'data': user_dict}
    else:
        return {'code': 514, 'data': {'msg': 'token is expired'}}


# 用户登出
@user_router.post('/logout', summary='用户登出')
@login_require
async def logout(request: Request):
    token = request.cookies.get('access_token', '')
    if token:
        try:
            # 销毁token并退出
            r.delete(token)
            return {'code': 200, 'data': {'msg': 'Logout success'}}
        except Exception as e:
            print(e)
            return {'code': 402, 'data': {'msg': 'Logout fail'}}
    else:
        return {'code': 508, 'data': {'msg': 'Illegal token'}}


# 获取用户列表
@user_router.get('/get_search_user', summary='获取用户列表')
@login_require
async def get_search_user(request: Request, name: Optional[str]):
    session = create_session()
    user_query = session.query(User).filter_by(name=name).all()
    user_list = []
    for item in user_query:
        temp_user = dict()
        temp_user['name'] = item.name
        user_list.append(item)
    session.close()
    return {'code': 200, 'data': {'items': user_list, 'msg': 'success'}}

# 测试
# @user_router.get('/get_form')
# @login_require
# async def get_form(request: Request):
#     return {'code': 200, 'data': {'msg': 'form_get_success'}}
