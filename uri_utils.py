#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
URL 主机解析
    >>> uri_host('http://192.168.0.1')
    'http://192.168.0.1/'
    >>> uri_host('http://user@192.168.0.1')
    'http://user@192.168.0.1/'
    >>> uri_host('http://user:pass@192.168.0.1')
    'http://user:pass@192.168.0.1/'
    >>> uri_host('http://user:pass@192.168.0.1:80')
    'http://user:pass@192.168.0.1:80/'
    >>> uri_host('http://user:pass@192.168.0.1:80/abc')
    'http://user:pass@192.168.0.1:80/'

URL 路径解析
    >>> uri_keyspace('http://192.168.0.1')
    ''
    >>> uri_keyspace('http://user@192.168.0.1')
    ''
    >>> uri_keyspace('http://user:pass@192.168.0.1')
    ''
    >>> uri_keyspace('http://user:pass@192.168.0.1:80')
    ''
    >>> uri_keyspace('http://user:pass@192.168.0.1:80/abc')
    'abc'
    >>> uri_keyspace('http://user:pass@192.168.0.1:80/abc/def')
    'abc/def'
    >>> uri_keyspace('http://user:pass@192.168.0.1:80/abc/def?ghi')
    'abc/def'
"""
import re

def parse_uri(uri):
    """
    @param uri: xxx://user:pass@host:port/database
    @return:
             {
                 schema: 'xxx',
                 username: 'user',
                 password: 'pass',
                 ipv6host: '',
                 ipv4host: 'host',
                 port: port,
                 keyspace: database
             }
     """
    pattern = re.compile(r"""
        (?P<schema>[\w\+]+)://
        (?:
            (?P<username>[^:/]*)
            (?::(?P<password>[^/]*))?
        @)?
        (?:
            (?:
                \[(?P<ipv6host>[^/]+)\] |
                (?P<ipv4host>[^/:]+)
            )?
            (?::(?P<port>[^/]*))?
        )?
        (?:/(?P<keyspace>[^?]*))?
        """, re.X)
    m = pattern.match(uri)
    if m is not None:
        components = m.groupdict()
        return components
    else:
        return {}


def uri_host(uri):
    """
    mysql://root:xbrother@localhost:3306/gu -> mysql://root:xbrother@localhost:3306/
    :param uri:
    :return: 主机地址
    """
    uri_dict = parse_uri(uri)
    if not uri_dict:
        return ''
    return '%(schema)s://%(user)s%(pass)s%(deli)s%(host)s%(port)s/' % {
            'schema': uri_dict['schema'],
            'user': uri_dict['username'] if uri_dict.get('username') else '',
            'pass': ':' + uri_dict['password'] if uri_dict.get('username') and uri_dict.get('password') else '',
            'deli': '@' if uri_dict.get('username') else '',
            'host': '[%s]' % uri_dict['ipv6host'] if uri_dict.get('ipv6host') else uri_dict['ipv4host'],
            'port': ':' + uri_dict['port'] if uri_dict.get('port') else ''
        }


def uri_keyspace(uri):
    """
    mysql://root:xbrother@localhost:3306/kv -> kv
    mysql://root:xbrother@localhost:3306/ -> ''
    http://root:xbrother@localhost/abc/def -> abc/def
    :param uri:
    :return:
    """
    uri_dict = parse_uri(uri)
    if not uri_dict:
        return ''
    if uri_dict['keyspace']:
        return uri_dict['keyspace']
    return ''


if __name__ == '__main__':
    import doctest
    doctest.testmod()
