#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 12:27:29 2019

@author: thomassullivan
"""

from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, and_, or_, not_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import select, insert, delete, update, func

from objects.objects2 import Article
from objects.objects2 import Category
import objects.BTCInput as BTCInput

connection = False

def connect():
    global connection, articles_table, categories_table
    if not connection:
        engine = create_engine("sqlite:///_db/articles.sqlite")
        meta = MetaData()
        meta.reflect(bind=engine)
        articles_table = meta.tables['Articles']
        categories_table = meta.tables['Categories']
        connection = engine.connect()
'''
 def __init__(self, id=0, name=None, year=0, month=0, category=None,
                 link=None, description=None):
        self.id = id
        self.name = name
        self.year = year
        self.month = month
        self.category = category
        self.link = link
        self.description = description'''

def close():
    if connection:
        connection.close()
        print('Database connection closed successfully')
    
#confirmed 
#def make_category(row):
#    return Category(row[0], row[1])

#confirmed
def make_category(row):
    return Category(id=row.categoryID, name=row.name)

#confirmed
#def make_article(row):
#    return Article(row[0], row[1], row[2],
#                   row[3], row[4], row[5],
#                   row[6])

#confirmed
def make_article(row):
    return Article(row["articleID"], row["name"], row["year"], row["month"],row["day"],
            get_category(row["categoryID"]),row["link"], row["description"],
            row["author"], row["publication"])

#select just one field: s = select([articles_table.c.name])
    
#def get_article(article_id):
#    s = select([articles_table]).where(articles_table.columns.articleID == article_id)
#    rp = connection.execute(s)
#    rp_tuple = tuple(rp)
#    rp_tuple = tuple(rp_tuple[0])
#    try:
#        new_article = make_article(rp_tuple)
#        return new_article
#    except TypeError:
#        return
    
def get_article(article_id):
    s = select([articles_table]).where(articles_table.columns.articleID == article_id)
    rp = connection.execute(s).fetchone()
    try:
        #ew_article = make_article(rp)
        new_article = Article.from_sqlalchemy(rp)
        return new_article
    except TypeError:
        return

#def get_category(category_id):
#    #returns a single category
#    s = select([categories_table.c.categoryID,
#        categories_table.c.name]).where(categories_table.c.categoryID == category_id)
#    rp = connection.execute(s)
#    try:
#        new_category = tuple(rp)[0] #take the single element out of nested tuple
#        new_category = make_category(new_category)
#        return new_category
#    except Exception as e:
#        print('Category not found:', e)
        
def get_category(category_id):
    #returns a single category
    s = select([categories_table.c.categoryID,
        categories_table.c.name]).where(categories_table.c.categoryID == category_id)
    rp = connection.execute(s).fetchone()
    try:
        #new_category = tuple(rp)[0] #take the single element out of nested tuple
        new_category = make_category(rp)
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
        categories_table.c.name]).where(categories_table.c.name.ilike("%{0}%".format(category_snippet)))
    rp = connection.execute(s).fetchone()
    try:
        #new_category = tuple(rp)[0] #take the single element out of nested tuple
        new_category = make_category(rp)
        return new_category
    except Exception as e:
        print('Category not found:', e)
        return

def get_categories():
    s = select([categories_table.c.categoryID, categories_table.c.name])
    rp = connection.execute(s)
    categories_collection = [make_category(cat) for cat in rp]
    return categories_collection
    #returns a list of categories

def get_all_articles():
    s = select([articles_table])
    rp = connection.execute(s)
    results = [make_article(i) for i in rp]
    return results

# =============================================================================
# The find_article_by_name function is intended to allow for partial name search functionality
# =============================================================================

def display_article_by_name(title_snippet):
    '''
    This function is intended to facilitate the search for articles using partial titles
    '''
    stmt = select([articles_table]).\
    where(articles_table.c.name.ilike("%{0}%".format(title_snippet)))
    
    rp = connection.execute(stmt).fetchone()
    try:
        article_by_name = make_article(rp)
        return article_by_name
    except Exception as e:
        print(e)
        return
    

def find_article_by_name(title_snippet):
    try:
        display_article_by_name(title_snippet)
    except Exception as e:
        print(e)
        return

#def get_articles_by_category(category_id):
#    s = select([articles_table]).where(articles_table.c.categoryID == category_id)
#    rp = connection.execute(s)
#    articles_by_category = [make_article(i) for i in rp]
#    return articles_by_category

def get_articles_by_category_id(category_id):
    s = select([articles_table]).where(articles_table.c.categoryID == category_id)
    rp = connection.execute(s)
    articles_by_category = [make_article(i) for i in rp]
    return articles_by_category

def get_articles_by_year(year):
    s = select([articles_table]).where(articles_table.c.year == year)
    rp = connection.execute(s)
    articles_by_year = [make_article(i) for i in rp]
    return articles_by_year

def get_articles_by_month(month, year):
    s = select([articles_table]).where(and_(articles_table.c.month == month,
              articles_table.c.year == year))
    rp = connection.execute(s).fetchall()
    articles_by_month = [make_article(i) for i in rp]
    return articles_by_month


def get_articles_by_date(day, month, year):
    s = select([articles_table]).where(and_(articles_table.c.month == month,
              articles_table.c.day == day, articles_table.c.year == year))
    rp = connection.execute(s)
    articles_by_date = [make_article(i) for i in rp]
    return articles_by_date

def get_articles_for_roundup(roundup_month, roundup_year, category_id):
    s = select([articles_table]).where(and_(articles_table.c.month == roundup_month,
              articles_table.c.year == roundup_year, articles_table.c.categoryID == category_id))
    rp = connection.execute(s)
    articles_for_roundup = [make_article(i) for i in rp]
    return articles_for_roundup

def finalize_descriptions(month, year):
    s = select([articles_table]).where(and_(articles_table.c.month == month,
              articles_table.c.year == year, articles_table.c.description=='Not specified'))
    rp = connection.execute(s)
    articles_for_finalizing = [make_article(i) for i in rp]
    return articles_for_finalizing

#def yearly_roundup_articles2(roundup_year):
#    pass
#
#def yearly_roundup_articles(roundup_year, category_id):
#    s = select([articles_table]).where(and_(articles_table.c.year == roundup_year,
#              articles_table.c.categoryID == category_id))
#    rp = connection.execute(s)
#    articles_for_roundup = [make_article(i) for i in rp]
#    return articles_for_roundup

def display_articles_by_author(author_snippet):
    '''
    This function is intended to facilitate the search for articles using partial author names
    '''
    stmt = select([articles_table]).\
    where(articles_table.c.author.ilike("%{0}%".format(author_snippet)))
    
    rp = connection.execute(stmt).fetchall()
    try:
        articles_by_author = [make_article(i) for i in rp]
        return articles_by_author
    except Exception as e:
        print(e)
        return

def display_articles_by_description(description_snippet):
    '''
    This function is intended to facilitate the search for articles using partial author names
    '''
    stmt = select([articles_table]).\
    where(articles_table.c.description.ilike("%{0}%".format(description_snippet)))
    
    rp = connection.execute(stmt).fetchall()
    try:
        articles_by_description = [make_article(i) for i in rp]
        return articles_by_description
    except Exception as e:
        print(e)
        return

def display_articles_by_publication(publication_snippet):
    '''
    This function is intended to facilitate the search for articles using partial author names
    '''
    stmt = select([articles_table]).\
    where(articles_table.c.publication.ilike("%{0}%".format(publication_snippet)))
    
    rp = connection.execute(stmt).fetchall()
    try:
        articles_by_publication = [make_article(i) for i in rp]
        return articles_by_publication
    except Exception as e:
        print(e)
        return

#will be used to generate reports of articles
def get_article_count(category_id):
    s = select([func.count(articles_table)]).where(articles_table.c.categoryID == category_id)
    rp = connection.execute(s)
    record = rp.first()
    return record.count_1

def get_yearly_article_count(category_id, year):
    #fix this
    s = select([func.count(articles_table)]).where(articles_table.c.categoryID == category_id and
              articles_table.c.year == year)
    rp = connection.execute(s)
    record = rp.first()
    return record.count_1


def get_monthly_article_count_old(category_id, month, year):
    s = select([func.count(articles_table)]).where(articles_table.c.categoryID == category_id and
              articles_table.c.month == month and articles_table.c.year == year)
    rp = connection.execute(s)
    record = rp.first()
    print(record.count_1)
    return record.count_1

def get_monthly_article_count(category_id, month, year):
    s = select([func.count(articles_table)]).where(and_(articles_table.c.categoryID == category_id,
              articles_table.c.month == month, articles_table.c.year == year))
    rp = connection.execute(s)
    record = rp.first()
    #print(record.count_1)
    return record.count_1

def get_undescribed_article_count(month, year):
    s = select([func.count(articles_table)]).where(articles_table.c.month == month
              and articles_table.c.year == year and articles_table.c.description == 'Not specified')
    rp = connection.execute(s)
    record = rp.first()
    return record.count_1

def add_article(article):
    ins = articles_table.insert().values(
            categoryID=article.category.id,
            name=article.name,
            year=article.year,
            month=article.month,
            day=article.day,
            link=article.link,
            description=article.description,
            author = article.author,
            publication = article.publication
            )
    result = connection.execute(ins)
    
def add_article_from_csv(article):
    ins = articles_table.insert().values(
            categoryID=article.category,
            name=article.name,
            year=article.year,
            month=article.month,
            day=article.day,
            link=article.link,
            description=article.description,
            author = article.author,
            publication = article.publication
            )
    result = connection.execute(ins)

def update_article_name(article_id, new_article_name):
    u = update(articles_table).where(articles_table.c.articleID == article_id)
    u = u.values(name=new_article_name)
    result = connection.execute(u)
    print(result.rowcount)

# =============================================================================
# def update_article_name(article_id, article_name):
#    sql = '''UPDATE article SET name = ?
#            WHERE articleID = ?'''
#    with closing(conn.cursor()) as c:
#        c.execute(sql, (article_name, article_id))
#        conn.commit()
# =============================================================================

def update_article_category(article_id, new_category):
    u = update(articles_table).where(articles_table.c.articleID == article_id)
    u = u.values(categoryID=new_category)
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

def update_article_date(article_id, new_day, new_month, new_year):
    u = update(articles_table).where(articles_table.c.articleID == article_id)
    u = u.values(day = new_day, month = new_month, year = new_year)
    result = connection.execute(u)
    print(result.rowcount)

def delete_article(article_id):
    u = delete(articles_table).where(articles_table.c.articleID == article_id)
    result = connection.execute(u)
    print(result.rowcount)
    
def add_category(category):
    category_name = category.name #takes a category object, so we have to get the name
    ins = categories_table.insert().values(name=category_name)
    result = connection.execute(ins)
    
def update_category(category_id, new_category_name):
    u = update(categories_table).where(categories_table.c.categoryID == category_id)
    u = u.values(name=new_category_name)
    result = connection.execute(u)

def delete_category(category_id):
    u = delete(categories_table).where(categories_table.c.categoryID == category_id)
    result = connection.execute(u)

 
if __name__ == '__main__':
    connect()

'''
articleID
categoryID
name
year
month
link
discipline
'''

# we can reflect it ourselves from a database, using options
# such as 'only' to limit what tables we look at...
#metadata.reflect(engine, only=['user', 'address'])

# ... or just define our own Table objects with it (or combine both)
#Table('user_order', metadata,
#                Column('id', Integer, primary_key=True),
#                Column('user_id', ForeignKey('user.id'))
#            )

# we can then produce a set of mappings from this MetaData.
#Base = automap_base(metadata=metadata)
#
## calling prepare() just sets up mapped classes and relationships.
#Base.prepare(engine, reflect=True)

# mapped classes are ready
#User, Address, Order = Base.classes.user, Base.classes.address,\
#    Base.classes.user_order
