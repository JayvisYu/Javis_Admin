# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MYSQL_PATH = "mysql+pymysql://root:123123@127.0.0.1:3306/jarvis_management?charset=utf8"


def create_session():
    engine = create_engine(MYSQL_PATH, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



