#from bs4 import BeautifulSoup
#import re
#import requests
import datetime
from typing import Any
from dataclasses import dataclass
#from dateutil.parser import parse
import news_article as na
#import db
#import tqdm
#from test_dal2 import dal
import BTCInput2 as btc

@dataclass
class Article:
    ArticleID: int = id
    name: str = None
    category: Any = None
    link: str = None
    description: str = None
    publication: str = None
    author: str = None
    date: datetime.date = None 
    
    article_months = {1:'January', 2: 'February', 3: 'March', 4: 'April',
                      5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September',
                      10: 'October', 11: 'November', 12: 'December'}
    #article_months is used to load csv files with the month name instead of a number
    
    @property
    def date_string(self):
        return self.date.strftime("%m/%d/%Y")
        #return self.date
        #template = '{0}/{1}/{2}'
        #return template.format(str(self.month), str(self.day).zfill(2), str(self.year))
    
    @staticmethod
    def get_date_formatted(article):
        result = article.date.strftime("%m/%d/%Y")
        #print(result)
        return result
    
    
    @classmethod
    def from_sqlalchemy(cls, articleID, name=None, date=None, categoryID=None, category_name=None,
                        link=None, description=None, publication=None, author=None):
        """
        Takes a RowProxy from sqlalchemy and returns an Article object. The argument
        names are the row names from the sqlalchemy database. These vary slightly
        from the attributes of the article object.
        """
        return cls(ArticleID=articleID, name=name, date=date,
                   category=Category(categoryID, category_name), link=link,
                   description=description, publication=publication, author=author)
        
    
    @classmethod
    def from_input(cls, link, category):
        try:
            print('Manual article creation')
            print('Press Ctrl+C to cancel')
            if not link:
                print('No link supplied, manual_add must be followed by link')
                return
                #link=read_text('Article url:' )
            name = btc.read_text('Article title: ')
            new_date = btc.read_date('Article date: ')
            #new_date = read_text('Article date: ')
            #new_date = parse(new_date)
            #assert Article.validate_date(day=day,month=month,year=year) == True
            author = btc.read_text('Author: ')
            publication = btc.read_text('Publication: ')
            category = category
            #category = category
            #if category == None:
            #    print('There is no category with that ID. article NOT added.\n')
            #    return
            #else:
            description = btc.read_text('Description: ')
            return cls(link=link, name=name, date=new_date,
                           author=author, publication=publication,
                           category=category, description=description)
        except Exception as e:
            print(e)
            return
                
            pass
        except KeyboardInterrupt:
            print('Ctrl+C pressed, add article cancelled')

    def manual_add(category, link=None):
        if (link == None) or (not link):
            print('Link', link)
            print('No link supplied, manual_add must be followed by link.')
            return
        else:
            print('Manual article creation/n')
            print('Link: {0}'.format(link))
            #Category.display_categories()
            #new_article_category = btc.read_int('Enter category for article: ')
            #category = db.get_category(new_article_category)
            assert category != None
            new_article = Article.from_input(link=link, category=category)
            if new_article == None:
                print('Article creation cancelled. Returning to main menu.')
                return
            return new_article
    
    @property
    def year(self):
        return self.date.year
    
    @property
    def month(self):
        return self.date.month
    
    @property
    def day(self):
        return self.date.day
    
    @property
    def url(self):
        return self.link
    
    @url.setter
    def url(self, text):
        self.link = text
    
    @property
    def title(self):
        return self.name
    
    @title.setter
    def title(self, text):
        self.name = text
    
    @property
    def month_text(self):
        return Article.article_months[self.month]

@dataclass
class Category:
    
    CategoryID: int = id
    category_name: str = None
    articles: Any = None
    
    @classmethod
    def from_input(cls):
        try:
            print('Manual category creation')
            print('Press "." to cancel')
            name = btc.read_text('Category name: ')
            #description = read_text('Description: ')
            return cls(category_name=name)
        except Exception as e:
            print(e)
            return
        except KeyboardInterrupt:
            print('Ctrl+C pressed, add category cancelled')

    @classmethod
    def from_sqlalchemy(cls, categoryID, category_name):
        """
        Takes a RowProxy from sqlalchemy and returns an Category object. The argument
        names are the row names from the sqlalchemy database. These vary slightly
        from the attributes of the article object.
        """
        return cls(CategoryID=categoryID, category_name=category_name, articles=None)
    
    @property
    def name(self):
        return self.category_name

class View:
    '''
    Shows the data about an article on the screen
    '''
    pass
    
#    @staticmethod
#    def display_categories(command=''):
#        del command
#        print("CATEGORIES")
#        categories = db.get_categories()  
#        for category in categories:
#            print(str(category.CategoryID) + ". " + category.category_name.strip(), end='   ')
#        print()

#    @staticmethod
#    def manual_add():
#        '''
#        Obtains a new Category object from the Category.from_input() method and
#        adds it to the database.
#        '''
#        new_category = Category.from_input()
#        if new_category.category_name != '.':
#            db.add_category(new_category)        
#            print('New category created: {0}'.format(new_category.name))
