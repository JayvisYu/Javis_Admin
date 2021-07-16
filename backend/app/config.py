# -*- coding:utf-8 -*-
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router


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

    # app.mount('/static', StaticFiles(directory='static'), name='static')
    # app.mount('/components', StaticFiles(directory='components'), name='components')
    app.mount('/models', StaticFiles(directory='models'), name='models')
    # app.mount('/data', StaticFiles(directory='data'), name='data')
    app.mount('/logs', StaticFiles(directory='logs'), name='logs')

    return app


ACCESS_TOKEN_EXPIRE_MINUTES = 60
# USERS = {
#     "john snow": {
#         "username": "john snow",
#         "full_name": "John Snow",
#         "email": "johnsnow@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }
# fake_users_db = {
#     "john snow": {
#         "username": "john snow",
#         "full_name": "John Snow",
#         "email": "johnsnow@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }
