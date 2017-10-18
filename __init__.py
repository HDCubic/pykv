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
        raise Exception('uri error')

if __name__ == '__main__':
    kv = KvFactory.new()
    print kv.set('test', 1)
    print kv.get('test')
    print kv.mset({'a': 'd', 'c': 'd'})
    print kv.mget(['a', 'c'])
    print kv.mget(['a', 'b', 'c'])
