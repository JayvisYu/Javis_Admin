# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from typing import Any, Union, Optional
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, constr
from passlib.context import CryptContext
from db.set_db import create_session
import jwt
from fastapi import Header
import time
import hashlib
import hmac

# 导入配置文件
import config

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 访问令牌过期时间


class UserInfo(BaseModel):
    username: str
    password: constr(min_length=6)


class Token(BaseModel):
    token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# 验证密码
def verify_password(plain_password: str, hashed_password: str):
    """对密码进行校验"""
    return pwd_context.verify(plain_password, hashed_password)


# 生成加密密码
def get_password_hash(password):
    return pwd_context.hash(password)


# 查询用户返回用户密码(加密过的)
def jwt_get_user(db, username: str):
    session = create_session()
    user_query = session.query(db).filter_by(username=username).first()
    session.close()
    user_dict = {}
    if user_query:
        user_dict['username'] = user_query.username
        user_dict['password'] = user_query.password
        user_dict['roles'] = [user_query.roles]
        user_dict['introduction'] = user_query.introduction
        user_dict['avator'] = user_query.avator
        user_dict['name'] = user_query.name
        user_dict['user_join_time'] = user_query.user_join_time
        return user_dict


# 验证用户
def jwt_authenticate_user(db, username: str, password: str):
    user = jwt_get_user(db=db, username=username)
    print(user)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user['password']):
        return False
    return user


# 创建token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 验证token
def get_sign(ak: str, nonce: str, ts: str, sk: str) -> str:
    """
    生成签名
    ak:也可以使用各自的id
    nonce:随机值
    ts:10位时间戳
    sk:secret加密用
    """
    # self.nonce = str(uuid.uuid1()).replace("-", "")
    # nonce = str(uuid.uuid1()).replace("-", "")
    a = [ak, nonce, ts]
    a.sort()
    # a = [self.ak, 'ZPMxNpPhmrPzQj27AGKijM3FmEcHW4BY', '1550032562']

    join_str = "".join(a)
    # print(join_str)
    return hmac.new(sk.encode(), join_str.encode(), hashlib.sha256).hexdigest()


async def token_is_true(server_id: str = Header(..., ), nonce: str = Header(..., ), timestamp: str = Header(..., ),
                        token: str = Header(..., description="token验证")):
    """签名验证，全局使用,超过60秒或者验证失败就会报错"""
    if time.time() - int(timestamp) > 60 or token == get_sign(server_id, nonce, timestamp, SECRET_KEY):
        raise HTTPException(
            status_code=401,
            detail="token is fail",
            headers={"X-Error": "There goes error"},
        )
    else:
        return {"msg": server_id}  # 可以自定义返回值，比如user或者其他的数据
