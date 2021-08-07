# -*- coding:utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from db.set_db import create_engine, create_session, DB_URI
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from datetime import datetime
import json

Base = declarative_base()


def init_permission_router_db():
    engine = create_engine(DB_URI, echo=False)
    Base.metadata.create_all(engine)


def drop_permission_router_db():
    engine = create_engine(DB_URI, echo=False)
    Base.metadata.drop_all(engine)


# 权限路由表
class PemissionRouter(Base):
    __tablename__ = 'permission_router'
    id = Column(Integer, primary_key=True, autoincrement=True)
    roles = Column(String(64))
    permission_routers = Column(String(200))
    join_time = Column(DateTime, default=datetime.now())  # 保存时间


if __name__ == '__main__':
    # 初始化数据库
    # init_permission_router_db()
    # 删除数据库
    drop_permission_router_db()

    # editor_permission_routers = {}
    # admin_permission_routers = {}
    #
    # # 添加用户
    # add_editor_data = PemissionRouter(roles=json.dumps(['editor']),
    #                                   permission_routers=json.dumps(editor_permission_routers))
    # add_admin_data = PemissionRouter(roles=json.dumps(['admin']),
    #                                  permission_routers=json.dumps(admin_permission_routers))
    # session = create_session()
    # session.add(add_editor_data)
    # session.add(add_admin_data)
    # session.commit()
    # session.close()
