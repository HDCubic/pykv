#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单例测试:
    >>> r1 = MemKv()

    >>> r2 = MemKv()

    >>> r1 is r2
    True

Mem连接测试:
    >>> r = MemConnection(host='localhost', port=6379)

    >>> r.set('k', 'v')

    >>> ret = r.get('k')

    >>> print ret[0], ret[1]
    v None

kv测试:
    >>> r = MemKv(host='localhost', port=6379)

    >>> r.set('k', 'v')

    >>> ret = r.get('k')

    >>> print ret[0], ret[1]
    v None
"""

import uri_utils
from single_ton import Singleton
from kv import KvInterface

class MemConnection(Singleton):
    def __init__(self, host='localhost', port=0):
        try:
            self.cache = {}
            return None
        except Exception as ee:
            return 'link error: %s' % ee.message

    def set(self, k, v):
        try:
            self.cache[k] = v
            return None
        except Exception as ee:
            return ee.message

    def get(self, k):
        try:
            return self.cache.get(k), None
        except Exception as ee:
            return None, ee.message

    def mset(self, kvs):
        try:
            self.cache.update(kvs)
            return None
        except Exception as ee:
            return ee.message

    def mget(self, ks):
        if not isinstance(ks, list):
            ks = [ks]
        try:
            return dict(map(lambda x: (x, self.cache.get(x)), ks)), None
        except Exception as ee:
            return None, ee.message

class MemKv(KvInterface, MemConnection):
    def __init__(self, host='localhost', port=6379):
        KvInterface.__init__(self)
        MemConnection.__init__(self, host=host, port=port)

    def set(self, k, v):
        return MemConnection.set(self, k, v)

    def get(self, k):
        return MemConnection.get(self, k)

    def mset(self, kvs):
        return MemConnection.mset(self, kvs)

    def mget(self, ks):
        return MemConnection.mget(self, ks)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

