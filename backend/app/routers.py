# -*- coding:utf-8 -*-
from fastapi import APIRouter

router = APIRouter()

from .views.users import login, info, logout, get_search_user
from .views.article import post_article_form

