#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单例测试:
    >>> r1 = RedisKv()

    >>> r2 = RedisKv()

    >>> r1 is r2
    True

Redis连接测试:
    >>> r = RedisConnection(host='localhost', port=6379)

    >>> r.set('k', 'v')

    >>> ret = r.get('k')

    >>> print ret[0], ret[1]
    v None

kv测试:
    >>> r = RedisKv(host='localhost', port=6379)

    >>> r.set('k', 'v')

    >>> ret = r.get('k')

    >>> print ret[0], ret[1]
    v None
"""
import redis

import uri_utils
from single_ton import Singleton
from kv import KvInterface

class RedisConnection(Singleton):
    def __init__(self, host='localhost', port=6379):
        try:
            self.r = redis.Redis(host=host, port=6379, db=0)
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

class RedisKv(KvInterface, RedisConnection):
    def __init__(self, host='localhost', port=6379):
        KvInterface.__init__(self)
        RedisConnection.__init__(self, host=host, port=port)

    def set(self, k, v):
        return RedisConnection.set(self, k, v)

    def mset(self, kvs):
        try:
            self.r.mset(kvs)
            return None
        except Exception as ee:
            return ee.message

    def get(self, k):
        return RedisConnection.get(self, k)

    def mget(self, ks):
        if not isinstance(ks, list):
            ks = [ks]
        try:
            vs = self.r.mget(ks)
            return dict(map(lambda x, y: (x, y), ks, vs)), None
        except Exception as ee:
            return '', ee.message

if __name__ == '__main__':
    import doctest
    doctest.testmod()

