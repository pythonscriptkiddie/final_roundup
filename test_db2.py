#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 20:39:38 2019

@author: thomassullivan
"""

from datetime import datetime, date
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, Date, ForeignKey, Boolean, create_engine,
                        CheckConstraint, insert, select, update, between,
                        startswith)

from objects import Article, Category
connection=False

def connect():
    global connection, articles_table, categories_table
    if not connection:
        engine = create_engine("sqlite:///db5.db")
        metadata = MetaData()
        articles_table = Table('Articles', metadata,
                Column('articleID', Integer(), primary_key=True, index=True),
                Column('name', String(200), default=None),
                Column('author', String(100), default=None),
                Column('publication', String(100), default=None),
                Column('link', String(200), default=None),
                Column('description', String(500), default=None),
                Column('date', Date(), default=None),
                Column('categoryID', ForeignKey('Categories.categoryID'))
                )
        categories_table = Table('Categories', metadata,
                   Column('categoryID', Integer(), primary_key=True),
                   Column('category_name', String(50), default=None)
                   )
        metadata.create_all(engine)
        connection = engine.connect()

def close():
    if connection:
        connection.close()
        print('database connection closed successfully')
        
    
def get_article(article_id):
    print(articles_table.c.articleID)
    columns= [articles_table.c.articleID, articles_table.c.name, articles_table.c.link, articles_table.c.date,
              articles_table.c.description, articles_table.c.categoryID, categories_table.c.category_name,
              articles_table.c.author, articles_table.c.publication]
    s = select(columns)
    s = s.select_from(articles_table.join(categories_table)).where(articles_table.c.articleID == article_id)
    rp = connection.execute(s).fetchone()
    try:
        #ew_article = make_article(rp)
        new_article = Article.from_sqlalchemy(articleID=rp.articleID, 
                                              name=rp.name, date=rp.date, 
                                              link=rp.link,
                                              description=rp.description,
                                              author=rp.author,
                                              categoryID = rp.categoryID,
                                              category_name = rp.category_name,
                                              publication=rp.publication)
        return new_article
    except TypeError:
        return

#metadata = MetaData()

if __name__ == '__main__':
    connect()


#engine = create_engine('sqlite:///db2.db')
#metadata.create_all(engine)
#connection = engine.connect()
