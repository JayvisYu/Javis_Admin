# -*- coding:utf-8 -*-
from fastapi import APIRouter
from utils.security import UserInfo, Token
from utils.security import create_access_token
from utils.decorators import login_require
from fastapi import HTTPException, Depends
from db.set_db import create_session
from db.set_redis import r, pool
from models.users import User
from starlette.requests import Request
from typing import Optional
from datetime import timedelta
import config

user_router = APIRouter()


# 用户登录
@user_router.post('/login', summary='用户登录', tags=['用户模块'])
async def login(user_info: UserInfo):
    session = create_session()
    user = session.query(User).filter_by(username=user_info.username).first()

    if user and user.check_user_password(user_info.password):
        # 如果用户正确通过 则生成token
        # 设置过期时间
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={'sub': user_info.username}, expires_delta=access_token_expires
        )
        user_id = user.id
        # redis存储用户的tokern信息
        r.set(access_token, user_id, ex=config.REDIS_EXPIRE_TIME)
        session.close()
        return {'code': 200, 'data': {'token': access_token, 'token_type': 'bearer'}}
    else:
        raise HTTPException(
            status_code=401,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        # return {'code': 401, 'data': {'msg': 'Incorrect username or password'}}


# token验证
@user_router.get('/info', summary='获取用户信息', tags=['用户模块'])
@login_require
async def info(request: Request, token: Optional[str]):
    # 判断token是否过期
    if r.get(token):
        user_id = r.get(token)
        session = create_session()
        user_query = session.query(User).filter_by(id=user_id).first()
        user_dict = dict()
        user_dict['username'] = user_query.username
        user_dict['roles'] = [user_query.roles]
        user_dict['introduction'] = user_query.introduction
        user_dict['avatar'] = user_query.avatar
        session.close()

        return {'code': 200, 'data': user_dict}
    else:
        return {'code': 514, 'data': {'msg': 'token is expired'}}


# 用户登出
@user_router.post('/logout', summary='用户登出', tags=['用户模块'])
@login_require
async def logout(request: Request):
    token = request.headers['authenticate']
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
@user_router.get('/get_search_user', summary='获取用户列表', tags=['用户模块'])
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
