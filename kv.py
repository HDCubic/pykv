#!/usr/bin/env python
# -*- coding: utf-8 -*-

class KvInterface(object):
    def __init__(self):
        pass

    def set(self, k, v):
        raise NotImplementedError

    def mset(self, kvs):
        raise NotImplementedError

    def get(self, k):
        raise NotImplementedError

    def mget(self, ks):
        raise NotImplementedError

