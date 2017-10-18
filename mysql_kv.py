#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单例测试:
    >>> r1 = MysqlKv()

    >>> r2 = MysqlKv()

    >>> r1 is r2
    True

Redis连接测试:
    >>> r = MysqlConnection(host='localhost', port=3306)

    >>> r.set('k', 'v')

    >>> ret = r.get('k')

    >>> print ret[0], ret[1]
    v None

kv测试:
    >>> r = MysqlKv(host='localhost', port=3306)

    >>> r.set('k', 'v')

    >>> ret = r.get('k')

    >>> print ret[0], ret[1]
    v None
"""

'''
import uri_utils
from single_ton import Singleton
from kv import KvInterface

class MysqlConnection(Singleton):
    def __init__(self, host='localhost', port=3306):
        try:
            self.r = redis.Redis(host=host, port=3306, db=0)
            return None
        except Exception as ee:
            return 'link error: %s' % ee.message

    def set(self, k, v):
        try:
            self.r.set(k, v)
            return None
        except Exception as ee:
            return ee.message

    def get(self, k):
        try:
            return self.r.get(k), None
        except Exception as ee:
            return '', ee.message

class MysqlKv(KvInterface, MysqlConnection):
    def __init__(self, host='localhost', port=3306):
        KvInterface.__init__(self)
        MysqlConnection.__init__(self, host=host, port=port)

    def set(self, k, v):
        pass

    def mset(self, kvs):
        pass

    def get(self, k):
        pass

    def mget(self, ks):
        if not isinstance(ks, list):
            ks = [ks]
        pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
'''
from sqlalchemy import *
from sqlalchemy.orm import *
#from sqlalchemy import (MetaData, Table, Column, Integer,
#                                Date, select, literal, and_, exists)

#功能:创建数据库表格，初始化数据库

#定义引擎
engine = create_engine('mysql://localhost:3306/testkv')
#绑定元信息
metadata = MetaData(engine)

#创建表格，初始化数据库
kv = Table('kv', metadata,
    Column('id', String(256), primary_key = True),
    Column('value', String(256))
)

#创建数据表，如果数据表存在则忽视！！！
metadata.create_all(engine)
#获取数据库链接，以备后面使用！！！！！
conn = engine.connect()

# insert
#insert = kv.insert().values({'id': 'test1', 'value': 'name'})
#print conn.execute(insert)

# upsert
#from sqlalchemy.dialects.mysql import insert
#print kv.insert().values({'id': 'test1', 'value': 'name'}).on_duplicate_key_update(value='update')
#conn.execute(upsert)
from sqlalchemy.dialects.mysql import insert

insert_stmt = insert(kv).values(
            id='test1',
            value='inserted value')

on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            value=insert_stmt.inserted.value
            )
print on_duplicate_key_stmt
conn.execute(on_duplicate_key_stmt)
