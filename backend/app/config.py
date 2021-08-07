# -*- coding:utf-8 -*-
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router
from starlette.middleware.sessions import SessionMiddleware

# 设置token过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 720
# 设置Redis过期时间(s)
REDIS_EXPIRE_TIME = ACCESS_TOKEN_EXPIRE_MINUTES * 60
SESSION_COOKIE_AGE = ACCESS_TOKEN_EXPIRE_MINUTES * 60


def create_app():
    app = FastAPI()

    app.include_router(router)
    # 添加中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # 是否关闭所有接口文档
    # app = FastAPI(docs_url=None, redoc_url=None)

    # app.add_middleware(SessionMiddleware, secret_key='Jarvis', max_age=SESSION_COOKIE_AGE)

    # app.mount('/static', StaticFiles(directory='static'), name='static')
    # app.mount('/components', StaticFiles(directory='components'), name='components')
    app.mount('/models', StaticFiles(directory='models'), name='models')
    # app.mount('/data', StaticFiles(directory='data'), name='data')
    app.mount('/logs', StaticFiles(directory='logs'), name='logs')

    return app
