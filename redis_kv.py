#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单例测试:
    >>> r1 = RedisKv()

    >>> r2 = RedisKv()

    >>> r1 is r2
    True

Redis连接测试:
    >>> r = RedisConnection('redis://localhost:6379')

    >>> r.set('k', 'v')

    >>> ret = r.get('k')

    >>> print ret[0], ret[1]
    v None

kv测试:
    >>> r = RedisKv('redis://localhost:6379')

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
    def __init__(self, uri='redis://localhost:6379'):
        try:
            uri_dict = uri_utils.parse_uri(uri)
            host = uri_dict['ipv6host'] if uri_dict.get('ipv6host') else uri_dict['ipv4host']
            port = uri_dict['port'] if uri_dict.get('port') else ''
            #print host, port
            self.r = redis.Redis(host=host, port=6379, db=0)
        except Exception as ee:
            return 'link error: %s' % ee.message

    def set(self, k, v):
        try:
            self.r.set(k, v)
        except Exception as ee:
            return ee.message

    def get(self, k):
        try:
            return self.r.get(k), None
        except Exception as ee:
            return '', ee.message

class RedisKv(KvInterface, RedisConnection):
    def __init__(self, uri='redis://localhost:6379'):
        KvInterface.__init__(self)
        RedisConnection.__init__(self, uri)

    def set(self, k, v):
        RedisConnection.set(self, k, v)

    def mset(self, kvs):
        raise NotImplementedError

    def get(self, k):
        return RedisConnection.get(self, k)

    def mget(self, ks):
        raise NotImplementedError

if __name__ == '__main__':
    import doctest
    doctest.testmod()

