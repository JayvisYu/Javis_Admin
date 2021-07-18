# -*- coding:utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from db.set_db import create_engine, create_session, DB_URI
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


def init_user_db():
    engine = create_engine(DB_URI, echo=False)
    Base.metadata.create_all(engine)


def drop_user_db():
    engine = create_engine(DB_URI, echo=False)
    Base.metadata.drop_all(engine)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    _password = Column(String(200), nullable=False)
    roles = Column(String(64), default=['editor'])
    introduction = Column(String(200))
    avatar = Column(String(200))
    name = Column(String(100))
    user_join_time = Column(DateTime, default=datetime.now())  # 保存时间

    def __init__(self, username, password, roles, introduction, avatar, name):
        self.username = username
        self.password = password
        self.roles = roles
        self.introduction = introduction
        self.avatar = avatar
        self.name = name

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_user_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result


# 密码: 对外的字段名叫做password
# 密码: 对内的字段名叫做_password


if __name__ == '__main__':
    # 初始化数据库
    # init_user_db()
    # 删除数据库
    # drop_user_db()

    # 添加用户
    add_editor_user = User(username='editor', password='123123', roles=['editor'],
                           introduction='I am an editor',
                           avatar='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                           name='Normal Editor')
    add_admin_user = User(username='admin', password='123123', roles=['admin'],
                          introduction='I am a super administrator',
                          avatar='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                          name='Super Admin')
    session = create_session()
    session.add(add_editor_user)
    session.add(add_admin_user)
    session.commit()
    session.close()
