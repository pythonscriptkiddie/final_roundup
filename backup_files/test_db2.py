#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 20:39:38 2019

@author: thomassullivan
"""

#from objects import Article, Category

from datetime import datetime, date
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, Date, ForeignKey, Boolean, create_engine,
                        CheckConstraint, insert, select,
                        update, and_, or_, not_)


from objects import Article, Category
from sqlalchemy.sql import delete, func
connection=False
#from test import testing

def connect():
    global connection, articles_table, categories_table
    if not connection:
        engine = create_engine("sqlite:///sub_saharan_roundup.db")
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
    '''
    This function takes a row from the database and makes a category.
    '''
    return Category(row[0], row[1])

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
    print(result.rowcount)
    
def add_article_from_csv(article):
    ins = articles_table.insert().values(
            categoryID=article.category,
            name=article.name,
            #print(article.name, 'caught by database'),
            date=article.date,
            link=article.link,
            description=article.description,
            author = article.author,
            publication = article.publication
            )
    result = connection.execute(ins)
    print(result.rowcount)
    
def add_category(category):
    category_name = category.name #takes a category object, so we have to get the name
    ins = categories_table.insert().values(category_name=category_name)
    result = connection.execute(ins)
    print(result.rowcount)

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
        print('Type error')
        return
    except AttributeError:
        print('Attribute error')
        return
    
def get_articles_by_id_range(starting_id, ending_id):
    print(articles_table.c.articleID)
    columns= [articles_table.c.articleID, articles_table.c.name, articles_table.c.link, articles_table.c.date,
              articles_table.c.description, articles_table.c.categoryID, categories_table.c.category_name,
              articles_table.c.author, articles_table.c.publication]
    s = select(columns)
    s = s.select_from(articles_table.join(categories_table)).where(and_(articles_table.c.articleID >= starting_id, 
                     articles_table.c.articleID <= ending_id))
    rp = connection.execute(s).fetchall()
    articles_by_id_range = [Article.from_sqlalchemy(articleID=row.articleID, 
                                              name=row.name, date=row.date, 
                                              link=row.link,
                                              description=row.description,
                                              author=row.author,
                                              categoryID = row.categoryID,
                                              category_name = row.category_name,
                                              publication=row.publication)
                                                for row in rp]
    #articles_by_id_range = [make_article(row) for row in rp]
    return articles_by_id_range

def get_articles_by_date(article_date):
    columns = [articles_table.c.articleID, articles_table.c.name, articles_table.c.link, articles_table.c.date,
              articles_table.c.description, articles_table.c.categoryID, categories_table.c.category_name,
              articles_table.c.author, articles_table.c.publication]
    s = select(columns)
    s = s.select_from(articles_table.join(categories_table)).where(articles_table.c.date == article_date)
    rp = connection.execute(s).fetchall()
    articles_by_date = [Article.from_sqlalchemy(articleID=row.articleID, 
                                              name=row.name, date=row.date, 
                                              link=row.link,
                                              description=row.description,
                                              author=row.author,
                                              categoryID = row.categoryID,
                                              category_name = row.category_name,
                                              publication=row.publication)
                                                for row in rp]
    return articles_by_date

def get_articles_by_date_range(start_date, end_date):
    columns = [articles_table.c.articleID, articles_table.c.name, articles_table.c.link, articles_table.c.date,
              articles_table.c.description, articles_table.c.categoryID, categories_table.c.category_name,
              articles_table.c.author, articles_table.c.publication]
    s = select(columns)
    s = s.select_from(articles_table.join(categories_table)).where(and_(articles_table.c.date >= start_date,
              articles_table.c.date <= end_date))
    #s = s.select_from(articles_table.join(categories_table)).where(articles_table.c.date == article_date)
    rp = connection.execute(s).fetchall()
    articles_by_date_range = [Article.from_sqlalchemy(articleID=row.articleID, 
                                              name=row.name, date=row.date, 
                                              link=row.link,
                                              description=row.description,
                                              author=row.author,
                                              categoryID = row.categoryID,
                                              category_name = row.category_name,
                                              publication=row.publication)
                                                for row in rp]
    #articles_by_date = [make_article(row) for row in rp]
    return articles_by_date_range

def get_categories():
    s = select([categories_table.c.categoryID, categories_table.c.category_name])
    rp = connection.execute(s)
    categories_collection=[Category.from_sqlalchemy(categoryID=i[0], category_name=i[1]) for i in rp]
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


def get_category_by_name(category_snippet):
    '''
    This function is intended to facilitate the search for articles by category using partial titles
    It gets the category by name and returns the articles by category if there is such a category.
    '''
    #returns a single category
    s = select([categories_table.c.categoryID,
        categories_table.c.category_name]).where(categories_table.c.category_name.ilike("%{0}%".format(category_snippet)))
    rp = connection.execute(s).fetchone()
    try:
        #new_category = tuple(rp)[0] #take the single element out of nested tuple
        #new_category = make_category(rp)
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
    #results = rp.fetchall()
    articles_for_roundup = [Article.from_sqlalchemy(articleID=row.articleID, 
                                              name=row.name, date=row.date, 
                                              link=row.link,
                                              description=row.description,
                                              author=row.author,
                                              categoryID = row.categoryID,
                                              category_name = row.category_name,
                                              publication=row.publication)
                                                for row in rp]
    return articles_for_roundup

def display_article_by_name(title_snippet):
    '''
    This function is intended to facilitate the search for articles using partial titles
    '''
    stmt = select([articles_table]).\
    where(articles_table.c.name.ilike("%{0}%".format(title_snippet)))
    
    rp = connection.execute(stmt).fetchone()
    try:
        #article_by_name = make_article(rp)
        article_by_name = Article.from_sqlalchemy(articleID=rp.articleID, 
                                                  name=rp.name, date=rp.date, 
                                                  link=rp.link,
                                                  description=rp.description,
                                                  author=rp.author,
                                                  categoryID = rp.categoryID,
                                                  category_name = rp.category_name,
                                                  publication= rp.publication)
        return article_by_name
    except Exception as e:
        print(e)
        return

def get_snippet(snippet, snippet_type, start_date=None, end_date=None):
    #if start_date:
     #   print(start_date)
    columns = [articles_table.c.articleID, articles_table.c.name, articles_table.c.link, articles_table.c.date,
          articles_table.c.description, articles_table.c.categoryID, categories_table.c.category_name,
          articles_table.c.author, articles_table.c.publication]
    s = select(columns)
    if snippet_type == 'title':
        #the snippet type is named title, but the field in the articles table is called name
        if (start_date == None) or (end_date == None):
            s = s.select_from(articles_table.join(categories_table)).where(articles_table.c.name.ilike("%{0}%".format(snippet)))
        else:
            print(start_date, end_date)
            s = s.select_from(articles_table.join(categories_table)).where(and_(articles_table.c.date >= start_date,
              articles_table.c.date <= end_date, articles_table.c.name.ilike("%{0}%".format(snippet))))
    elif snippet_type == 'description':
        if (start_date == None) or (end_date == None):
            s = s.select_from(articles_table.join(categories_table)).where(articles_table.c.description.ilike("%{0}%".format(snippet)))
        else:
            s = s.select_from(articles_table.join(categories_table)).where(and_(articles_table.c.date >= start_date,
              articles_table.c.date <= end_date, articles_table.c.description.ilike("%{0}%".format(snippet))))
        #s = s.select_from(articles_table.join(categories_table)).where(articles_table.c.description.ilike("%{0}%".format(snippet)))
    elif snippet_type == 'category':
        if (start_date == None) or (end_date == None):
            s = s.select_from(articles_table.join(categories_table)).where(categories_table.c.category_name.ilike("%{0}%".format(snippet)))
        else:
            s = s.select_from(articles_table.join(categories_table)).where(and_(articles_table.c.date >= start_date,
              articles_table.c.date <= end_date, categories_table.c.category_name.ilike("%{0}%".format(snippet))))
    elif snippet_type == 'category_id':
        if (start_date == None) or (end_date == None):
            s = s.select_from(articles_table.join(categories_table)).where(categories_table.c.categoryID == snippet)
        else:
            s = s.select_from(articles_table.join(categories_table)).where(and_(articles_table.c.date >= start_date,
              articles_table.c.date <= end_date, categories_table.c.categoryID==snippet))
        pass
    else:
        print('Incorrect snippet type, return to main menu')
        return
    rp = connection.execute(s).fetchall()
    articles_by_snippet = [Article.from_sqlalchemy(articleID=row.articleID, 
                                              name=row.name, date=row.date, 
                                              link=row.link,
                                              description=row.description,
                                              author=row.author,
                                              categoryID = row.categoryID,
                                              category_name = row.category_name,
                                              publication=row.publication)
                                                for row in rp]
    return articles_by_snippet
    
def display_articles_by_category_id(start_date, end_date, category_id):
    columns = [articles_table.c.articleID, articles_table.c.name, articles_table.c.date,
                articles_table.c.categoryID, articles_table.c.link,
                articles_table.c.description, articles_table.c.publication,
                articles_table.c.author, categories_table.c.category_name]
    s = select(columns)
    s = s.select_from(articles_table.join(categories_table)).where(and_(articles_table.c.date >= start_date,
              articles_table.c.date <= end_date, categories_table.c.categoryID==category_id))
              #articles_table.c.year == roundup_year, articles_table.c.categoryID == category_id))
    rp = connection.execute(s)
    #results = rp.fetchall()
    
    articles_by_categoryID = [Article.from_sqlalchemy(articleID=row.articleID, 
                                              name=row.name, date=row.date, 
                                              link=row.link,
                                              description=row.description,
                                              author=row.author,
                                              categoryID = row.categoryID,
                                              category_name = row.category_name,
                                              publication=row.publication)
                                                for row in rp]
    return articles_by_categoryID
    
def display_articles_by_publication(publication_snippet):
    '''
    This function is intended to display articles based on partial publication
    titles.
    '''
    columns = [articles_table.c.articleID, articles_table.c.name, articles_table.c.link, articles_table.c.date,
              articles_table.c.description, articles_table.c.categoryID, categories_table.c.category_name,
              articles_table.c.author, articles_table.c.publication]
    s = select(columns)
    s = s.select_from(articles_table.join(categories_table)).where(articles_table.c.publication.ilike("%{0}%".format(publication_snippet)))
    rp = connection.execute(s).fetchall()
    articles_by_name = []
    for i in rp:
        new_article = Article.from_sqlalchemy(articleID=i.articleID, 
                                                  name=i.name, date=i.date, 
                                                  link=i.link,
                                                  description=i.description,
                                                  author=i.author,
                                                  categoryID = i.categoryID,
                                                  category_name = i.category_name,
                                                  publication=i.publication)
        articles_by_name.append(new_article)
    return articles_by_name

def display_articles_by_author(author_snippet):
    '''
    This function is intended to display articles based on partial publication
    titles.
    '''
    columns = [articles_table.c.articleID, articles_table.c.name, articles_table.c.link, articles_table.c.date,
              articles_table.c.description, articles_table.c.categoryID, categories_table.c.category_name,
              articles_table.c.author, articles_table.c.publication]
    s = select(columns)
    s = s.select_from(articles_table.join(categories_table)).where(articles_table.c.author.ilike("%{0}%".format(author_snippet)))
    rp = connection.execute(s).fetchall()
    articles_by_name = []
    for i in rp:
        new_article = Article.from_sqlalchemy(articleID=i.articleID, 
                                                  name=i.name, date=i.date, 
                                                  link=i.link,
                                                  description=i.description,
                                                  author=i.author,
                                                  categoryID = i.categoryID,
                                                  category_name = i.category_name,
                                                  publication=i.publication)
        articles_by_name.append(new_article)
    return articles_by_name

def get_undescribed_article_count(start_date, end_date, description_snippet):
    #def get_date_range_article_count(category_id, start_date, end_date):
    s = select([func.count(articles_table)]).where(and_(articles_table.c.description.ilike("%{0}%".format(description_snippet)),
              articles_table.c.date >= start_date, articles_table.c.date <= end_date))
    rp = connection.execute(s)
    record = rp.first()
    #print(record.count_1)
    return record.count_1

def get_count(snippet):
    pass
    

def get_article_count(category_id=None, start_date=None, end_date=None):
    if (start_date == None) and (end_date == None):
        s = select([func.count(articles_table)]).where(articles_table.c.categoryID == category_id)
    elif (category_id == None):
        s = select([func.count(articles_table)]).where(and_(articles_table.c.date >= start_date,
                  articles_table.c.date <= end_date))
    elif (category_id==None) and (start_date==None) and (end_date==None):
        print('Invalid entry')
        return
    else:    
        s = select([func.count(articles_table)]).where(and_(articles_table.c.categoryID == category_id,
                  articles_table.c.date >= start_date, articles_table.c.date <= end_date))
    rp = connection.execute(s)
    record = rp.first()
    return record.count_1

#UPDATE SECTION - Update articles and categories

def update_article_name(article_id, new_article_name):
    u = update(articles_table).where(articles_table.c.articleID == article_id)
    u = u.values(name=new_article_name)
    result = connection.execute(u)
    print(result.rowcount)

def update_article_description(article_id, new_description):
    u = update(articles_table).where(articles_table.c.articleID == article_id)
    u = u.values(description=new_description)
    result = connection.execute(u)
    print(result.rowcount)
    
def update_article_author(article_id, new_author):
    u = update(articles_table).where(articles_table.c.articleID == article_id)
    u = u.values(author=new_author)
    result = connection.execute(u)
    print(result.rowcount)
    
def update_article_publication(article_id, new_publication):
    u = update(articles_table).where(articles_table.c.articleID == article_id)
    u = u.values(publication = new_publication)
    result = connection.execute(u)
    print(result.rowcount)
    
def update_article_category(article_id, new_category):
    u = update(articles_table).where(articles_table.c.articleID == article_id)
    u = u.values(categoryID=new_category)
    result = connection.execute(u)
    print(result.rowcount)

def update_article_date(article_id, new_date):
    u = update(articles_table).where(articles_table.c.articleID == article_id)
    u = u.values(date=new_date)
    result = connection.execute(u)
    print(result.rowcount)
    
def update_category(category_id, new_category_name):
    '''Updates the name of a category'''
    u = update(categories_table).where(categories_table.c.categoryID == category_id)
    u = u.values(category_name = new_category_name)
    result = connection.execute(u)
    print(result.rowcount)

#DELETE SECTION - Delete articles and categories
    
def delete_item(item_id, item_type):
    if item_type == 'article':
        u = delete(articles_table).where(articles_table.c.articleID == item_id)
    elif item_type == 'category':
        u = delete(categories_table).where(categories_table.c.categoryID == item_id)
    else:
        print('Invalid delete command. Return to main menu.')
    result = connection.execute(u)
    print(result.rowcount)
        

if __name__ == '__main__':
    connect()
