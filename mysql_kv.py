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

import uri_utils
from single_ton import Singleton
from kv import KvInterface

# rely on sqlalchemy>=1.2
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.dialects.mysql import insert

class MysqlConnection(Singleton):
    def __init__(self, host='localhost', port=3306):
        try:
            engine = create_engine('mysql://%s:%s/testkv' % (host, port))
            metadata = MetaData(engine)

            self.kv = Table('kv', metadata,
                Column('id', String(256), primary_key = True),
                Column('value', String(256))
            )

            metadata.create_all(engine)
            self.conn = engine.connect()
        except Exception as ee:
            return 'link error: %s' % ee

    def set(self, k, v):
        try:

            insert_stmt = insert(self.kv).values(id=k, value=v)
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(value=insert_stmt.inserted.value)
            self.conn.execute(on_duplicate_key_stmt)
        except Exception as ee:
            return ee.message

    def get(self, k):
        try:
            query = select([self.kv.c.id, self.kv.c.value]).where(self.kv.c.id==k)
            result = self.conn.execute(query).fetchone()
            if result:
                return result[1], None
            return None, None
        except Exception as ee:
            return None, ee.message

    def mset(self, kvs):
        try:
            insert_stmt = insert(self.kv).values([(k, v) for k, v in kvs.iteritems()])
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(value=insert_stmt.inserted.value)
            self.conn.execute(on_duplicate_key_stmt)
        except Exception as ee:
            return ee.message

    def mget(self, ks):
        if not isinstance(ks, list):
            ks = [ks]
        try:
            query = select([self.kv.c.id, self.kv.c.value]).where(self.kv.c.id.in_(ks))
            ret = self.conn.execute(query).fetchall()
            if ret:
                result = dict(ret)
            extra_ks = set(ks) - set(result.keys())
            result.update(dict(map(lambda x: (x, None), extra_ks)))
            return result, None
        except Exception as ee:
            return None, ee.message


class MysqlKv(KvInterface, MysqlConnection):
    def __init__(self, host='localhost', port=3306):
        KvInterface.__init__(self)
        MysqlConnection.__init__(self, host=host, port=port)

    def set(self, k, v):
        return MysqlConnection.set(self, k, v)

    def get(self, k):
        return MysqlConnection.get(self, k)

    def mset(self, kvs):
        return MysqlConnection.mset(self, kvs)

    def mget(self, ks):
        return MysqlConnection.mget(self, ks)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    ##m = MysqlConnection()
    #m = MysqlKv()
    #m.set('k', 'v1')
    #print m.get('k')
    #print m.get('k1')
    #print m.mset({'a': 'b', 'b': 'c'})
    #print m.mget(['a', 'b'])
    #print m.mget(['a', 'b', 'c'])
