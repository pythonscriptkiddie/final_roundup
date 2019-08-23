#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 20:39:38 2019

@author: thomassullivan
"""

from datetime import datetime, date
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, Date, ForeignKey, Boolean, create_engine,
                        CheckConstraint, insert, select, update, and_, or_, not_)

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

def make_category(row):
    #print(row[0], row[1])
    return Category(row[0], row[1])

def make_article(row):
    '''
    The variables in this code are incontruous with the rest of the program.
    result_zero was added to save time cutting and pasting.
    '''
    try:
        assert type(row == dict), 'Converting article to dictionary format.'
    #result_zero = dict(row)
        result_zero = row
        test = Article(ArticleID=result_zero['articleID'], category=Category.from_sqlalchemy(result_zero['categoryID'], result_zero['category_name']),
                       link = result_zero['link'], description= result_zero['description'], date=result_zero['date'], publication=result_zero['publication'],
                       author=result_zero['author'], name=result_zero['name'])
        return test
    except AssertionError:
        result_zero = dict(row)
        test = Article(ArticleID=result_zero['articleID'], category=Category.from_sqlalchemy(result_zero['categoryID'], result_zero['category_name']),
                       link = result_zero['link'], description= result_zero['description'], date=result_zero['date'], publication=result_zero['publication'],
                       author=result_zero['author'], name=result_zero['name'])
        return test

#CREATE section - create articles and categories

def add_article(article):
    ins = articles_table.insert().values(
            categoryID=article.category.CategoryID,
            name=article.name,
            date=article.date,
            link=article.link,
            description=article.description,
            author = article.author,
            publication = article.publication
            )
    result = connection.execute(ins)

#READING SECTION - read/get articles and categories
    
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
    

def get_categories():
    s = select([categories_table.c.categoryID, categories_table.c.category_name])
    rp = connection.execute(s)
    categories_collection=[]
    for i in rp:
        #print(i, type(i))
        t = Category.from_sqlalchemy(categoryID=i[0], category_name=i[1])
        t = make_category(i)
        categories_collection.append(t)
    return categories_collection

def get_category(category_id):
    #returns a single category
    s = select([categories_table.c.categoryID,
        categories_table.c.category_name]).where(categories_table.c.categoryID == category_id)
    rp = connection.execute(s).fetchone()
    try:
        new_category = Category.from_sqlalchemy(categoryID=rp[0], category_name=rp[1])
        return new_category
    except Exception as e:
        print('Category not found:', e)
        return


def get_articles_for_roundup(start_date, end_date, category_id):
    columns = [articles_table.c.articleID, articles_table.c.name, articles_table.c.date,
                articles_table.c.categoryID, articles_table.c.link,
                articles_table.c.description, articles_table.c.publication,
                articles_table.c.author, categories_table.c.category_name]
    s = select(columns)
    s = s.select_from(articles_table.join(categories_table)).where(and_(articles_table.c.date >= start_date,
              articles_table.c.date <= end_date, categories_table.c.categoryID==category_id))
              #articles_table.c.year == roundup_year, articles_table.c.categoryID == category_id))
    rp = connection.execute(s)
    results = rp.fetchall()
    articles_for_roundup = []
    for i in results:
        #print(i)
        #new_article = Article.from_sqlalchemy(i)
        articles_for_roundup.append(i)
        
    article_dict_list = [dict(i) for i in articles_for_roundup]
   # We make a dictionary so that we can make an article with it using
   # make_article
    
    new_articles = []
    for item in article_dict_list:
        new_articles.append(make_article(item))
        
    return new_articles


#UPDATE SECTION - Update articles and categories

if __name__ == '__main__':
    connect()


#engine = create_engine('sqlite:///db2.db')
#metadata.create_all(engine)
#connection = engine.connect()
