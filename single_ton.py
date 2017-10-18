#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    >>> s1 = Singleton()

    >>> s2 = Singleton()

    >>> s1 is s2
    True
"""

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

if __name__ == '__main__':
    import doctest
    doctest.testmod()
