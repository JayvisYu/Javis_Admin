# -*- coding:utf-8 -*-
from ..routers import router
from ..utils.decorators import login_require
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, Depends
from pydantic import BaseModel, constr
from db.set_db import create_session
from db.set_redis import r, pool
from ..models.articles import Article
from starlette.requests import Request
from typing import Optional
from datetime import timedelta
import config


class FormData(BaseModel):
    id: Optional[str] = None
    author: str
    content: str
    content_short: str
    display_time: str
    importance: int
    status: str
    title: str


class ListQuery(BaseModel):
    page: int
    limit: int


# 提交文章
@router.post('/api/post_article_form', summary='提交文章', tags=['文章模块'])
@login_require
async def post_article_form(request: Request, data: FormData):
    receive_form_data = jsonable_encoder(data)
    add_data = Article(author=receive_form_data['author'],
                       title=receive_form_data['title'],
                       content=receive_form_data['content'],
                       content_short=receive_form_data['content_short'],
                       display_time=receive_form_data['display_time'],
                       importance=receive_form_data['importance'],
                       status=receive_form_data['status'])
    session = create_session()
    try:
        session.add(add_data)
        session.commit()
        session.close()
        return {'code': 200, 'data': {'msg': 'success'}}
    except Exception as e:
        print(e)
        session.close()
        return {'code': 500, 'data': {'msg': 'add data failed'}}


# 获取文章列表
@router.post('/api/get_article_list', summary='获取文章列表', tags=['文章模块'])
@login_require
async def get_article_list(request: Request, data: ListQuery):
    receive_form_data = jsonable_encoder(data)
    print(receive_form_data)
    if receive_form_data:
        page = receive_form_data['page']
        limit = receive_form_data['limit']
        session = create_session()
        total_data_query = session.query(Article).all()
        total = len(total_data_query)
        article_list_query = session.query(Article).limit(limit).offset((int(page) - 1) * limit)
        article_list = list()
        for item in article_list_query:
            temp_dict = dict()
            temp_dict['id'] = item.id
            temp_dict['author'] = item.author
            temp_dict['title'] = item.title
            temp_dict['content'] = item.content
            temp_dict['content_short'] = item.content_short
            temp_dict['timestamp'] = item.display_time
            temp_dict['importance'] = item.importance
            temp_dict['status'] = item.status
            article_list.append(temp_dict)
        session.close()
        return {'code': 200, 'data': {'msg': 'success', 'total': total, 'article_list': article_list}}
    else:
        return {'code': 500, 'data': {'msg': 'get article list failed'}}
