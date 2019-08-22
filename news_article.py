#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 05:44:38 2019

@author: thomassullivan
"""

from newspaper import Article as NewsItem
#from objects import Article

def get_article_from_url(url):
    new_article = NewsItem(url=url)
    new_article.download()
    new_article.build()
    new_article.nlp()
    #print(new_article.__dict__)
    #print(new_article)
    return new_article

def get_title(new_article):
    return new_article.title

def get_article_title(url):
    try:
        new_article = get_article_from_url(url)
        return get_title(new_article)
    except Exception as e:
        title = 'Not found due to {0}'.format(e)
        return title

def get_summary(new_article):
    return new_article.summary

def get_article_summary(url):
    try:
        new_article = get_article_from_url(url)
        return get_summary(new_article)
    except Exception as e:
        description = 'Not found due to {0}'.format(e)
        return description
        

if __name__ == '__main__':
    new_link = input('Please enter the link: ' )
    new_article = get_article_from_url(new_link)
    print(new_article.url)