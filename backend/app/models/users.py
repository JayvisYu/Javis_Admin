# -*- coding:utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from db.set_db import create_engine, MYSQL_PATH
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
import time
import os

Base = declarative_base()


def init_user_db():
    engine = create_engine(MYSQL_PATH, echo=False)
    Base.metadata.create_all(engine)


def drop_user_db():
    engine = create_engine(MYSQL_PATH, echo=False)
    Base.metadata.drop_all(engine)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    username = Column(String(64), unique=True)
    password = Column(String(64))
    avator = Column(String(64))
    introduction = Column(String(64))
    user_save_time = Column(DateTime, default=datetime.now())  # 保存时间


if __name__ == '__main__':
    init_user_db()
    # drop_user_db()
