# -*- coding:utf-8 -*-
from fastapi import APIRouter

router = APIRouter()

from .views.users import login

