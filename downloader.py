#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 10:23:17 2019

@author: thomassullivan
"""
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
import newspaper
from newspaper import Article
#from urllib.request import urlopen

class NewsItem(object):
    def __init__(self, url):
        self.newsItemID = id
        self.url = url
        self.Article = None
        self._is_downloaded = False
    
    def download(self):
        article = Article(self.url)
        self.Article = article
        self._is_downloaded = True

    def set(self, value):
        self.var = value

    def get(self):
        return self.var


def change_obj_value(obj):
    obj.set(100)


if __name__ == '__main__':
    BaseManager.register('NewsItem', NewsItem)
    manager = BaseManager()
    manager.start()
    inst = manager.NewsItem()

    p = Process(target=change_obj_value, args=[inst])
    p.start()
    p.join()

    print(inst)                    # <__main__.SimpleClass object at 0x10cf82350>
    print(inst.get())