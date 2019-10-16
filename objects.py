#from bs4 import BeautifulSoup
#import re
#import requests
import datetime
from typing import Any
from dataclasses import dataclass
from dateutil.parser import parse
import news_article as na
#import db
#import tqdm
#from test_dal2 import dal
import BTCInput2 as btc
#import ui

#pd.options.display.max_colwidth = 200

DEBUG_MODE = True

def read_text(prompt):
    '''
    Displays a prompt and reads in a string of text.
    Keyboard interrupts (CTRL+C) are ignored
    returns a string containing the string input by the user
    '''
    while True:  # repeat forever
        try:
            result=input(prompt) # read the input
            # if we get here no exception was raised
            if result=='':
                #don't accept empty lines
                print('Please enter text')
            else:
                # break out of the loop
                break
        except KeyboardInterrupt:
            # if we get here the user pressed CTRL+C
            print('Please enter text')
            if DEBUG_MODE:
                raise Exception('Keyboard interrupt')

    # return the result
    return result


def read_number(prompt,function):
    '''
    Displays a prompt and reads in a floating point number.
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns a float containing the value input by the user
    '''
    while True:  # repeat forever
        try:
            number_text=read_text(prompt)
            result=function(number_text) # read the input
            # if we get here no exception was raised
            # break out of the loop
            break
        except ValueError:
            # if we get here the user entered an invalid number
            print('Please enter a number')

    # return the result
    return result

def read_number_ranged(prompt, function, min_value, max_value):
    '''
    Displays a prompt and reads in a number.
    min_value gives the inclusive minimum value
    max_value gives the inclusive maximum value
    Raises an exception if max and min are the wrong way round
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns a number containing the value input by the user
    '''
    if min_value>max_value:
        # If we get here the min and the max
        # are wrong way round
        raise Exception('Min value is greater than max value')
    while True:  # repeat forever
        result=read_number(prompt,function)
        if result<min_value:
            # Value entered is too low
            print('That number is too low')
            print('Minimum value is:',min_value)
            # Repeat the number reading loop
            continue 
        if result>max_value:
            # Value entered is too high
            print('That number is too high')
            print('Maximum value is:',max_value)
            # Repeat the number reading loop
            continue
        # If we get here the number is valid
        # break out of the loop
        break
    # return the result
    return result

def read_float(prompt):
    '''
    Displays a prompt and reads in a floating point number.
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns a float containing the value input by the user
    '''
    return read_number(prompt,float)

def read_int(prompt):
    '''
    Displays a prompt and reads in an integer number.
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns an int containing the value input by the user
    '''
    return read_number(prompt,int)

def read_float_ranged(prompt, min_value, max_value):
    '''
    Displays a prompt and reads in a floating point number.
    min_value gives the inclusive minimum value
    max_value gives the inclusive maximum value
    Raises an exception if max and min are the wrong way round
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns a number containing the value input by the user
    '''
    return read_number_ranged(prompt,float,min_value,max_value)

def read_int_ranged(prompt, min_value, max_value):
    '''
    Displays a prompt and reads in an integer point number.
    min_value gives the inclusive minimum value
    max_value gives the inclusive maximum value
    Raises an exception if max and min are the wrong way round
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns a number containing the value input by the user
    '''
    return read_number_ranged(prompt,int,min_value,max_value)

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
            name = read_text('Article title: ')
            new_date = btc.read_date('Article date: ')
            #new_date = read_text('Article date: ')
            #new_date = parse(new_date)
            #assert Article.validate_date(day=day,month=month,year=year) == True
            author = read_text('Author: ')
            publication = read_text('Publication: ')
            category = category
            #category = category
            #if category == None:
            #    print('There is no category with that ID. article NOT added.\n')
            #    return
            #else:
            description = read_text('Description: ')
            return cls(link=link, name=name, date=new_date,
                           author=author, publication=publication,
                           category=category, description=description)
        except Exception as e:
            print(e)
            return
                
            pass
        except KeyboardInterrupt:
            print('Ctrl+C pressed, add article cancelled')
    
#    @classmethod
#    def from_newspaper(cls, link):
#        '''
#        Adds an article from the newspaper module after downloading it
#        '''
#        for i in tqdm.tqdm(range(1)):
#            try:
#                newNewsItem = na.get_article_from_url(link)
#            except:
#                print('Article download failed, invalid URL')
#                print('Returning to main menu')
#                return
#        print(newNewsItem)
#        try:
#            name = newNewsItem.title #get the title for the article
#        except Exception as e:
#            print(e)
#            name = btc.read_text('Please enter title: ')
#            #get article author
#        try:
#            author = ' '.join(newNewsItem.authors)
#            #get article publication
#        except Exception as e:
#            print(e)
#            author = btc.read_text('Please enter author: ')
#        try:
#            #works for most websites, but not Sudan Tribune
#            publication = newNewsItem.meta_data['og']['site_name']
#        except Exception as e:
#            print(e)
#            publication = btc.read_text('Please enter publication: ')
#        try:
#            year = newNewsItem.publish_date.year
#            month = newNewsItem.publish_date.month
#            day = newNewsItem.publish_date.day
#            new_date = datetime.date(day=day, month=month, year=year)
#        except Exception as e:
#            print(e)
#            has_date = False
#            while has_date == False:
#                try:
#                    new_date = btc.read_text('Enter article date MM/DD/YYYY: ')
#                    new_date = parse(new_date)
#                    new_date = new_date.date()
#                    has_date = True
#                except Exception as e:
#                    print(e)
#            
#        except Exception as e:
#            print('invalid date', e)
#        try:
#            summary = newNewsItem.summary
#        except Exception as e:
#            print(e)
#            print('Summary download failed')
#            summary = 'Summary not found'
#        try:
#            keywords = ', '.join(newNewsItem.keywords)
#        except Exception as e:
#            print(e)
#            print('Keyword download failed')
#            keywords= 'keywords not found'
#        print('TITLE - {0} - AUTHOR {1}'.format(name, author))
#        print('DATE - {0} - PUBLICATION {1}'.format(new_date.strftime("%m/%d/%Y"), publication))
#        print('KEYWORDS: ', keywords)
#        Category.display_categories()
#        category_id = btc.read_text("Category ID: ")
#        category = db.get_category(category_id)
#        if category == None:
#            print('There is no category with that ID. article NOT added.\n')
#            return
#        description_choice = btc.read_text('View article description? y/n: ')
#        if description_choice == 'y':
#            print('Title: {0}'.format(name))
#            print('Summary: {0}'.format(summary))
#            print('Keywords: {0}'.format(keywords))
#        description = btc.read_text("Description or '.' to cancel: ")
#        
#        if description == ".":
#            return
#        else:
#            return cls(name=name, date=new_date,
#                      category=category, link=link, description=description,
#                      author=author, publication=publication)
        
#    @staticmethod
#    def add_from_newspaper(link):
#        new_article = Article.from_newspaper(link)
#        db.add_article(new_article)    
#        print(new_article.name + " was added to database.\n")
#            article = Article(name=name, date=new_date,
#                      category=category, link=link, description=description,
#                      author=author, publication=publication)
#        db.add_article(article)    
#        print(name + " was added to database.\n")

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
#            db.add_article(new_article)
#            print(new_article.title + " was added to database.\n")
    
        
    #def __repr__(self):
    #    template = 'id:{0}, name:{1}, date{2}, cat:{3}'
    #   return template.format(self.ArticleID, self.name, self.category)
    
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
            name = read_text('Category name: ')
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
