#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单例测试:
    >>> r1 = MongoKv()

    >>> r2 = MongoKv()

    >>> r1 is r2
    True

Mongo连接测试:
    >>> r = MongoConnection(host='localhost', port=27017)

    >>> r.set('k', 'v')

    >>> ret = r.get('k')

    >>> print ret[0], ret[1]
    v None

kv测试:
    >>> r = MongoKv(host='localhost', port=27017)

    >>> r.set('k', 'v')

    >>> ret = r.get('k')

    >>> print ret[0], ret[1]
    v None
"""
import pymongo
from pymongo import UpdateOne

import uri_utils
from single_ton import Singleton
from kv import KvInterface

class MongoConnection(Singleton):
    def __init__(self, host='localhost', port=27017):
        try:
            conn = pymongo.MongoClient(host=host, port=int(port))
            db = conn.kv
            self.kv = db.kv
            return None
        except Exception as ee:
            return 'link error: %s' % ee.message

    def set(self, k, v):
        try:
            self.kv.update({'_id': k}, {'$set': {'_id': k, 'value': v}}, upsert=True, multi=False)
            return None
        except Exception as ee:
            return ee.message

    def get(self, k):
        try:
            ret = self.kv.find_one({'_id': k})
            print ret
            if ret:
                return ret['value'], None
            return None, None
        except Exception as ee:
            return None, ee.message

    def mset(self, kvs):
        try:
            requests = []
            for k, v in kvs.iteritems():
                requests.append(UpdateOne({'_id': k}, {'$set': {'_id': k, 'value': v}}, upsert=True))
            self.kv.bulk_write(requests, ordered=False)
            return None
        except Exception as ee:
            return ee.message

    def mget(self, ks):
        if not isinstance(ks, list):
            ks = [ks]
        try:
            ret = self.kv.find({'_id': {'$in': ks}})
            result = dict(map(lambda x: (x['_id'], x['value']), ret))
            extra_ks = set(ks) - set(result.keys())
            result.update(dict(map(lambda x: (x, None), extra_ks)))
            return result, None
        except Exception as ee:
            return None, ee.message

class MongoKv(KvInterface, MongoConnection):
    def __init__(self, host='localhost', port=27017):
        KvInterface.__init__(self)
        MongoConnection.__init__(self, host=host, port=port)

    def set(self, k, v):
        return MongoConnection.set(self, k, v)

    def get(self, k):
        return MongoConnection.get(self, k)

    def mset(self, kvs):
        return MongoConnection.mset(self, kvs)

    def mget(self, ks):
        return MongoConnection.mget(self, ks)

if __name__ == '__main__':
    import doctest
    #doctest.testmod()
    m = MongoConnection()
    print m.set('k', 'v')
    print m.get('k')
    print m.get('v')
    print m.mset({'a': 'b', 'c': 'd'})
    print m.mget(['a', 'b', 'c', 'd'])

