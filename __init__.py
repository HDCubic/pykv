#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uri_utils

class KvFactory:

    @staticmethod
    def new(uri='redis://localhost:6379'):
        params = uri_utils.parse_uri(uri)
        schema = params['schema']

        if schema == 'redis':
            from redis_kv import RedisKv
            host = params['ipv6host'] if params.get('ipv6host') else params['ipv4host']
            port = params['port'] if params.get('port') else ''
            return RedisKv(host, port)

        if schema == 'mysql':
            from mysql_kv import MysqlKv
            host = params['ipv6host'] if params.get('ipv6host') else params['ipv4host']
            port = params['port'] if params.get('port') else ''
            return MysqlKv(host, port)

        if schema == 'mongodb':
            from mongo_kv import MongoKv
            host = params['ipv6host'] if params.get('ipv6host') else params['ipv4host']
            port = params['port'] if params.get('port') else ''
            return MongoKv(host, port)

        if schema == 'mem':
            from mem_kv import MemKv
            return MemKv()

        raise Exception('uri error')

if __name__ == '__main__':
    #kv = KvFactory.new('mysql://localhost:3306')
    #kv = KvFactory.new('redis://localhost:6379')
    #kv = KvFactory.new('mongodb://localhost:27017')
    kv = KvFactory.new('mem://localhost')
    print kv.set('test', '1')
    print kv.get('test')
    print kv.mset({'a': 'd', 'c': 'd'})
    print kv.mget(['a', 'c'])
    print kv.mget(['a', 'b', 'c'])

    import time

    def time_used(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            ret = func(*args, **kwargs)
            end_time = time.time()
            print '%s used %ss' % (func.__name__, end_time-start_time)
            return ret
        return wrapper
    # 性能测试

    @time_used
    def test_set(n):
        kv = KvFactory.new('mysql://localhost:3306')
        #kv = KvFactory.new('redis://localhost:6379')
        #kv = KvFactory.new('mongodb://localhost:27017')
        #kv = KvFactory.new('mem://localhost')
        for i in xrange(n):
            kv.set(str(i), str(i))

    @time_used
    def test_get(n):
        kv = KvFactory.new('mysql://localhost:3306')
        #kv = KvFactory.new('redis://localhost:6379')
        #kv = KvFactory.new('mongodb://localhost:27017')
        #kv = KvFactory.new('mem://localhost')
        for i in xrange(n):
            kv.get(str(i))

    #test_set(100000)
    test_get(100000)
