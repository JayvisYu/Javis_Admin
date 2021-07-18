# -*- coding:utf-8 -*-
from fastapi import HTTPException, status
from db.set_redis import r, pool
from starlette.requests import Request
from functools import wraps


def login_require(func):
    @wraps(func)
    async def inner(request: Request, *args, **kwargs):
        if r.get(request.headers['authenticate']):
            return await func(request, *args, **kwargs)
        else:
            # raise HTTPException(
            #     status.HTTP_401_UNAUTHORIZED,
            #     # detail="Incorrect username or password",
            #     detail="用户未登录",
            #     headers={"WWW-Authenticate": "Bearer"},
            # )
            return {'code': 401, 'data': {'msg': 'please login first'}}

    return inner
