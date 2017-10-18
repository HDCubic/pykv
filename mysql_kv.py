#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    >>> kv = MysqlKv('mysql://root@localhost:3306/kv')
    mysql kv
    >>> kv.set('2', '3')

    >>> print kv.get('2')
    3
"""
from kv import KvInterface

class MysqlKv(KvInterface):
    def __init__(self, uri='mysql://root@localhost:3306/kv'):
        print 'mysql', 'kv'

    def set(self, k, v):
        raise NotImplementedError()

    def mset(self, k, v):
        raise NotImplementedError()

    def get(self, k):
        raise NotImplementedError()

    def mget(self, ks):
        raise NotImplementedError()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
