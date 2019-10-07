#!/usr/bin/env/python3

'''
5/22/19 - Get article titles using BeautifulSoup

'''

import db
from objects import Article, Category
import roundup_docx2 as roundup_docx
import BTCInput as btc
import operator
import csv
import glob
import cmd
import sys
import news_article as na
import datetime
#import tqdm
from matplotlib import pyplot as plt
from dateutil.parser import parse


'''perhaps create a menu that appears when you choose the edit article option
then gives you choice of what to edit'''

        
def display_menu(title, menu_items, end='   '):
    print(title.upper())
    for i in menu_items:
        print(i, end=end)

#def display_categories(command=''):
#    del command
#    Category.display_categories()
#    del command
#    print("CATEGORIES")
#    categories = db.get_categories()  
#    for category in categories:
#        print(str(category.CategoryID) + ". " + category.category_name.strip(), end='   ')
#    print()

def display_single_article(article, title_term):
    template ='''
ARTICLE ID - {0}\tARTICLE TITLE: {1}
AUTHOR: {2}\tPUBLICATION: {3}'''
    

    print(template.format(title_term, article.title, article.author, article.publication))
    print("-" * 155)
    template2 = "Category: {0}\nDate: {1}\nDescription: {2}\nLink: {3}"

    print(template2.format(article.category.category_name, article.date_string,
                                 article.description, article.link))  
    print()

    
def display_articles(articles, title_term):
    print("ARTICLES - " + title_term)
    line_format = "{0:3s} {1:50s}\t{2:10s} {3:10}\t{4:35s} {5:35s}"
    print(line_format.format("ID", "Name", "Category", 'Date', "Description","Link"))
    print("-" * 155)
    for article in articles:
        print(line_format.format(str(article.ArticleID), article.name.lstrip()[:50],
                                 article.category.category_name[:10], article.date_string,
                                 article.description[:35], article.link[:35]))                          
    print()

def display_articles_by_name(title_snippet=None):
    if not title_snippet:
        title_snippet = btc.read_text('Enter article title or "." to cancel: ')
    if title_snippet != '.':
        #result = db.display_article_by_name(title_snippet)
        results = db.get_articles_by_name(title_snippet)
        if results == None:
            print('There is no article with that name.\n')
        else:
            display_articles(results, str('Results for {0}'.format(title_snippet)))
    else:
        print('Search cancelled, returning to main menu.')
        
def display_articles_by_description(description_snippet=None):
    if not description_snippet:
        description_snippet = btc.read_text('Enter article title or "." to cancel: ')
    if description_snippet != '.':
        #result = db.display_article_by_name(title_snippet)
        results = db.get_articles_by_description(description_snippet)
        if results == None:
            print('There is no article with that name.\n')
        else:
            display_articles(results, str('Results for {0}'.format(description_snippet)))
    else:
        print('Search cancelled, returning to main menu.')

def display_articles_by_category_id(category_id, start_date, end_date):
    category = db.get_category(category_id)
    if category == None:
        print("There is no category with that ID.\n")
    else:
        print()
        articles = db.display_articles_by_category_id(start_date, end_date, category_id)
        print('Number of articles:', len(articles))
        display_articles(articles, category.category_name.upper())
        print('Total articles: {0}'.format(db.get_article_count(category_id=category_id,
              start_date=start_date, end_date=end_date)))

def display_articles_by_category_name(category_snippet, start_date, end_date):
    search_category = db.get_category_by_name(category_snippet)
    if search_category == None:
        print('There is no category with that ID.\n')
    else:
        print()
        #search_category_id = search_category.CategoryID
        articles = db.display_articles_by_category_name(start_date, end_date, category_snippet)
        display_articles(articles, search_category.category_name.upper())
 
def search_single_date(article_date):
    assert type(article_date) == datetime.date
    #article_date = parse(article_date)
    #new_date = article_date.date()
    #print(type(new_date))
    if article_date == None:
        print('Date entered incorrectly')
    else:
        articles = db.get_articles_by_date(article_date)
        formatted_date = article_date.strftime("%m/%d/%Y")
        #print(articles)
        display_articles(articles, formatted_date)
        
def search_date_range(start_date, end_date):
    try:
        assert start_date <= end_date
    except AssertionError:
        print('Start date must come before end date')
        return
    articles = db.get_articles_by_date_range(start_date, end_date)
    formatted_start_date = start_date.strftime("%m/%d/%Y")
    formatted_end_date = end_date.strftime("%m/%d/%Y")
    display_articles(articles, str('{0} to {1}'.format(formatted_start_date,
                                   formatted_end_date)))    
    
def display_article_by_id(article_id=None):
    if not article_id:
        article_id = input("Article ID: ")
    article = db.get_article(article_id)
    if article == None:
        print("There is no article with that ID. article NOT found.\n")
    else:
        print()
        display_single_article(article, str(article.ArticleID))
        
def display_article_by_id_range(starting_id, ending_id):
    try:
        assert starting_id <= ending_id
    except AssertionError:
        print('Starting ID must be less than ending ID. Return to main menu.')
        return
    articles = db.get_articles_by_id_range(starting_id, ending_id)
    if articles == None:
        print('No articles were found in that ID range.')
    else:
        print()
        display_articles(articles, str('{0} {1}'.format(starting_id, ending_id)))
    
        
def display_articles_by_author(author_snippet=None):
    if not author_snippet:
        author_snippet = btc.read_text("Author Name: ")
    articles = db.display_articles_by_author(author_snippet)
    if articles == None:
        print("There are no articles by that author. article NOT found.\n")
    else:
        print()
        display_articles(articles, "AUTHOR: " + str(articles[0].author))

def display_articles_by_publication(publication_snippet=None):
    if not publication_snippet:
        publication_snippet = btc.read_text("Publication: ")
    publications = db.display_articles_by_publication(publication_snippet)
    if publications == None:
        print("There are no articles by that publication. article NOT found.\n")
        return
    else:
        print()
        try:
            display_articles(publications, "PUBLICATION: " + str(publications[0].publication))
        except IndexError as e:
            display_articles(publications, "PUBLICATION: " + str('Error: {0}'.format(e)))

def manual_add(link=None):
    Article.manual_add(link)
    

def update_article_name(article_id):
    article = db.get_article(article_id)
    if article == None:
        print("There is no article with that ID. article NOT found.\n")
    else:
        print()
        display_single_article(article, str(article.ArticleID))
        article_choice = btc.read_int_ranged('1 to edit article title, 2 to leave as is: ' ,
                                             min_value = 1, max_value = 2)
        if article_choice == 1:
            try:
                newsItem1 = na.get_article_from_url(article.link)
                updated_title = newsItem1.title
            except Exception as e:
                print('Scrape failed because of {0}'.format(e))
                updated_title = 'Invalid'
            print('Rescraped title: {0}'.format(updated_title))
            title_choice = btc.read_int_ranged('1 - existing title, 2 - scraped title, 3 - manual input: ', 1, 3)
                                
            if title_choice == 1:
                print('Title update cancelled, article title unchanged.')
                return
            elif title_choice == 2:
                db.update_article_name(article_id, updated_title)
                print('Title update complete. Return to main menu.')
            elif title_choice == 3:
                new_title = btc.read_text('Enter new title or . to cancel: ')
                if new_title != '.':
                    db.update_article_name(article_id, new_title)
                else:
                    print('Edit cancelled, return to main menu')
                    return
        else:
            print('Edit cancelled, article title unchanged')
            
def update_article_category(article_id):
    article = db.get_article(article_id)
    if article == None:
        print("There is no article with that ID. article NOT found.\n")
    else:
        print()
        display_single_article(article, str(article.ArticleID))
        article_choice = btc.read_int_ranged('1 to edit article category, 2 to leave as is: ' ,
                                             min_value = 1, max_value = 2)
        if article_choice == 1:
            new_category_id = btc.read_int('Enter new category_id: ')
            result = db.get_category(new_category_id)
            #Add in some text that is displayed to make it clear that the category is being updated
            if result == None:
                print('There is no category with that ID, article category NOT updated.\n')
            else:
                db.update_article_category(article_id, new_category_id)
        else:
            print('Edit cancelled, article title unchanged')
            
def update_article_description(article_id):
    article = db.get_article(article_id)
    if article == None:
        print("There is no article with that ID. article NOT found.\n")
    else:
        print()
        display_single_article(article, str(article.ArticleID))
        article_choice = btc.read_int_ranged('1 to edit article description, 2 to leave as is: ' ,
                                             min_value = 1, max_value = 2)
        if article_choice == 1:
            description_choice = btc.read_text('View article description? y/n: ')
            if description_choice == 'y':
                article_summary = na.get_article_summary(article.link)
                print(article_summary)
            new_description = btc.read_text('Enter new description or "." to cancel: ')
            
            if new_description != '.':
                db.update_article_description(article_id, new_description)
                print('Article description updated.\n')
            else:
                print('Edit cancelled, article description unchanged')
        else:
            print('Edit cancelled, article description unchanged')

def update_article_author(article_id):
    article = db.get_article(article_id)
    if article == None:
        print("There is no article with that ID. article NOT found.\n")
    else:
        print()
        display_single_article(article, str(article.ArticleID))
        article_choice = btc.read_int_ranged('1 to edit article author, 2 to leave as is: ' ,
                                             min_value = 1, max_value = 2)
        if article_choice == 1:
            new_author = btc.read_text('Enter new author name or . to cancel: ')
            if new_author != '.':
                db.update_article_author(article_id, new_author)
        else:
            print('Edit cancelled, article title unchanged')

def update_article_publication(article_id):
    article = db.get_article(article_id)
    if article == None:
        print("There is no article with that ID. article NOT found.\n")
    else:
        print()
        display_single_article(article, str(article.ArticleID))
        article_choice = btc.read_int_ranged('1 to edit article publication, 2 to leave as is: ' ,
                                             min_value = 1, max_value = 2)
        if article_choice == 1:
            new_publication = btc.read_text('Enter new publication name or . to cancel: ')
            if new_publication != '.':
                db.update_article_publication(article_id, new_publication)
                print(article_id, new_publication)
        else:
            print('Edit cancelled, article title unchanged')

def update_article_date(article_id):
    article = db.get_article(article_id)
    if article == None:
        print("There is no article with that ID. article NOT found.\n")
    else:
        print()
        display_single_article(article, str(article.ArticleID))
        article_choice = btc.read_int_ranged('1 to edit article date, 2 to leave as is: ' ,
                                             min_value = 1, max_value = 2)
        if article_choice == 1:
            new_date = btc.read_text('Enter new date:' )
            new_date = parse(new_date)
            new_date_format = new_date.date()
            print(type(new_date))
            date_choice = btc.read_int_ranged('1 to change date to: {0}, 2 to cancel: '.format(new_date_format),
                                              min_value=1, max_value=2)
            if date_choice == 1:
                db.update_article_date(article_id, new_date)
                print('Update complete.\n')
            elif date_choice == 2:
                print('Edit cancelled, article date unchanged')
        else:
            print('Edit cancelled, article date unchanged')

def scrape_article_name(article_id):
    article = db.get_article(article_id)
    if article == None:
        print('There is no article with that ID. article NOT found.\n')
    else:
        print()
        display_single_article(article, str(article.ArticleID))
        article_choice = btc.read_int_ranged('1 to rescrape title, 2 to leave as is: ',
                                             min_value = 1, max_value = 2)
        if article_choice == 1:
            try:
                new_article_news_item = na.get_article_from_url(article.link)
                new_title = new_article_news_item.title
                print('''
New title: {0}
Old title: {1}'''.format(new_title, article.name))
            except:
                new_title = 'Title scrape failed'
            title_choice = btc.read_int_ranged('1 to replace title, 2 to keep original title: ',
                                               min_value = 1, max_value = 2)
            if title_choice == 1:
                db.update_article_name(article_id, new_title)
            elif title_choice == 2:
                print('article update cancelled')
                
        elif article_choice == 2:
            print('article update cancelled')
    
def finalize_article_descriptions(start_date, end_date):
    undescribed = db.get_date_range_undescribed_articles(description_snippet='Not specified',
                                                         start_date=start_date,
                                                         end_date=end_date)
    undescribed_articles = len(undescribed)
    print('Total undescribed articles: {0}'.format(undescribed_articles))
    for article in undescribed:
        print('Undescribed articles remaining: {0}'.format(undescribed_articles))
        update_article_description(article.ArticleID)
        undescribed_articles -= 1
        description_choice = btc.read_int_ranged('{0} descriptions remaining. Press 1 to continue, 2 to cancel: '.format(undescribed_articles), 1, 2)
        if description_choice == 2:
            print('Update descriptions cancelled')
            break
        
#add function to finalize articles for one month
def finalize_desc_month(command):
    if not command or command == '':
        new_month = btc.read_int_ranged('Enter new month: ', min_value = 1, max_value = 12)
        new_year = btc.read_int_ranged('Enter new year: ', min_value = 1, max_value = 2100)
        articles_to_finalize = db.get_articles_by_month(month=new_month, year=new_year)
        articles_remaining = len(articles_to_finalize)
        for article in articles_to_finalize:
            print('{0} unreviewed articles'.format(articles_remaining))
            
            update_article_description(article.ArticleID)
            description_choice = btc.read_int_ranged('{0} descriptions remaining. Press 1 to continue, 2 to cancel: '.format(articles_remaining),
                                                     1, 2)
            
            articles_remaining -= 1
            if description_choice == 2:
                print('Update descriptions cancelled')
                break

        
def finalize_title_updates(month, year):
    articles = db.get_articles_by_month(month=month, year=year)
    articles_remaining = len(articles)
    for article in articles:
        print('{0} articles remaining'.format(articles_remaining))
        display_single_article(article, title_term = article.ArticleID)
        strip_choice = btc.read_int_ranged('1 to update title, 2 to skip, 3 to return to main menu: ', 1, 3)
        if strip_choice == 1:
            update_article_name(article.ArticleID)
            articles_remaining -= 1
        if strip_choice == 2:
            articles_remaining -= 1
            print('Article title unchanged.')
        if strip_choice == 3:
            print('strip titles cancelled')
            #display_title()
            break

def get_category_chart(start_date, end_date):
    #get the data from the database
    #calculate how many of the articles have been described
    categories = db.get_categories()
    categories = db.get_categories()
    start_date_pretty = start_date.strftime("%m/%d/%Y")
    end_date_pretty = end_date.strftime("%m/%d/%Y")
    #total_articles = len(db.get_articles_by_date_range(start_date,
    #                                                   end_date))
    category_info = [[category.category_name,
                     db.get_article_count(category_id=category.CategoryID,
                                                  start_date=start_date,
                                                  end_date=end_date)] for category in categories]
    category_names = [i[0] for i in category_info]
    article_numbers = [i[1] for i in category_info]
    #create bar chart
    plt.bar(range(len(category_names)), article_numbers)
    plt.title('Articles per category from {0} to {1}'.format(start_date_pretty,
              end_date_pretty))
    plt.ylabel('# of articles') #label the y-axis
               
    #label x-axis with movies at bar centers
    plt.xticks(range(len(category_names)), category_names)
    plt.show()
    
               
def get_date_range_category_stats(start_date, end_date):
    '''
    The roundups must have at least a few articles in each category. This
    function gets the stats for the categories between a start date and an
    end date input by the user.
    '''
    categories = db.get_categories()
    total_articles = db.get_article_count(start_date=start_date,
                                                       end_date=end_date)
    category_ids = [[category.CategoryID, category.category_name,
                     db.get_article_count(category_id=category.CategoryID,
                                                  start_date=start_date,
                                                  end_date=end_date)] for category in categories]
    category_ids = sorted(category_ids, key=operator.itemgetter(2), reverse=True)
    undescribed_articles = db.get_undescribed_article_count(description_snippet='Not specified',
                                                            start_date = start_date,
                                                            end_date = end_date)
    #print(len(undescribed_articles))
    #undescribed_articles = len(undescribed_articles)
    print('{0} articles are undescribed'.format(undescribed_articles))
    try:
        percent_incomplete = (undescribed_articles/total_articles)*100
        total_articles_completed = 100
        percent_incomplete = total_articles_completed - percent_incomplete
        print('CATEGORY STATS')
        print('-'*64)
        line_format = '{0:<3} {1:11s} \t{2:10}'
        print('{0:<3} {1:11s} {2:10}'.format('ID', 'Name', '\tQty.'))
        print('-'*64)
        for item in category_ids:
            print(line_format.format(item[0], item[1], str(item[2])))
        print('-'*64)
        print('Undescribed Articles: {0} (Completed: {1:.2f} percent)'.format(undescribed_articles,
              percent_incomplete))
        print('Total Articles: {0}'.format(total_articles))
    except ZeroDivisionError as e:
        print(e)
        return
    
def get_category_id(category_name):
    '''Takes the category name and returns the category ID'''
    new_category = db.get_category_by_name(category_name)
    category_id = new_category.CategoryID
    return category_id
    
def get_csv_in_directory():
    file_list = glob.glob('*.csv')
    print('Files available: ')
    for item in file_list:
        print(item, end='\n')
    #try:
    importing_file_name = btc.read_text('Enter filename from the list or ". " to cancel: ')
    if importing_file_name != '.':
        filename='{0}.csv'.format(importing_file_name)
        csv_articles = create_csv_list(filename)
        print(csv_articles)
        print('Articles to import:')
        try:
            for article in csv_articles:
                try:
                    csv_article = csv_item_to_article(article)
                    db.add_article_from_csv(csv_article)
                    print(csv_article.name + " was added to database.\n")
                except IndexError:
                    print('Add article failed')
            print('Import complete, return to main menu')
        except TypeError:
            print('File not found')
            return

def create_csv_list(filename):
    csvRows = []
    try:
        csvFileObj = open(filename)
        readerObj = csv.reader(csvFileObj)
    except FileNotFoundError:
        print('File not found, return to main menu')
        return
    print('csv reader created')
    for row in readerObj:
        if readerObj.line_num == 1:
            continue
        csvRows.append(row)
    csvFileObj.close()
    print('csv list created')
    return csvRows
    
def csv_item_to_article(csv_list_item):
    new_article_news_item = na.get_article_from_url(csv_list_item[0])
    new_article_link = new_article_news_item.url
    new_article_title = new_article_news_item.title
    print(new_article_title)
    new_article_category = get_category_id(csv_list_item[1])
    new_article_datetime = parse(csv_list_item[2])
    new_article_date = new_article_datetime.date()

    article_from_csv = Article(name=new_article_title,link=new_article_link, category=new_article_category, date=new_article_date,
                               description='Not specified', author='Not specified', publication='Not specified')
    return article_from_csv
    
def delete_article(article_id):
    try:
        article = db.get_article(article_id)
        choice = input("Are you sure you want to delete '" + 
                       article.name + "'? (y/n): ")
        if choice == "y":
            db.delete_article(article_id)
            print("'" + article.name + "' was deleted from database.\n")
        else:
            print("'" + article.name + "' was NOT deleted from database.\n")
    except AttributeError as e:
        print(e, 'Article id not found')

def add_category():
    '''
    Planned change: move manual category creation code to the objects.py file
    '''
    Category.manual_add()

        
def update_category(category_id=0):
    if category_id == 0:
        category_id = int(input("category ID: "))
    category = db.get_category(category_id)
    articles = db.get_articles_by_category_id(category_id)
    display_articles(articles, category.category_name.upper())
    new_category_name = btc.read_text("Enter new category name or '.' to cancel: ")
    if new_category_name != '.':
        update_choice = btc.read_int_ranged("1 to change article name to {0}, 2 to cancel: ".format(new_category_name),
                                            1, 2)
        if update_choice == 1:
            db.update_category(category_id, new_category_name)
            print('Category update complete\n')
        elif update_choice == 2:
            print('Update cancelled.\n')

def delete_category():
    category_id = int(input("category ID: "))
    articles_in_category = db.get_article_count(category_id=category_id,
                                                           start_date=None,
                                                           end_date=None)
    if articles_in_category > 0:
        print('Category contains articles, cannot be deleted')
    elif articles_in_category == 0:
        delete_choice = btc.read_float_ranged('Press 1 to delete, 2 to cancel: ', 1, 2)
        if delete_choice == 1:
            db.delete_category(category_id)
            print('Category deleted.\n')
        elif delete_choice == 2:
            print('Delete cancelled, returning to category menu')

def export_roundup():
    roundup_title = btc.read_text('Enter the roundup title or "." to cancel: ')
    filename = btc.read_text('Enter the filename or "." to cancel: ')
    if roundup_title != '.':
        roundup_categories = db.get_categories()
        for category in roundup_categories:
            category.articles = db.get_articles_by_category_id(category.id)
        roundup_docx.create_complete_roundup(filename=filename, roundup_title=roundup_title, categories=roundup_categories)
        
def export_roundup_by_date():
    roundup_title = btc.read_text('Enter the roundup title: ')
    start_date = parse(btc.read_text('Enter the starting date: '))
    start_date = start_date.date()
    #start_date = parse(start_date)
    end_date = parse(btc.read_text('Enter the ending date: '))
    end_date = end_date.date()
    print('start date: ', start_date, 'end date: ', end_date)
    print('start date type:', type(start_date), 'end date type:', type(end_date))
    filename = btc.read_text('Enter roundup filename: ')
    roundup_choice = btc.read_int_ranged('Enter 1 to export roundup, 2 to cancel: ', 1, 2)
    if roundup_choice == 1:
        roundup_categories = db.get_categories()
        for category in roundup_categories:
            #category.articles = db.get_articles_for_roundup(roundup_month, roundup_year, category.id)
            category.articles = db.get_articles_for_roundup(start_date, end_date, category.CategoryID)
            print(len(category.articles))
        roundup_docx.create_complete_roundup(filename=filename, roundup_title=roundup_title, categories=roundup_categories)
        #display_title()
    elif roundup_choice == 2:
        print('Roundup export cancelled. Return to main menu.\n')
        #display_title()
        
def export_roundup_by_category():
    #display_categories()
    Category.display_categories()
    roundup_categories = db.get_categories()
    categories_remaining = len(roundup_categories)
    categories_for_roundup = []
    for category in roundup_categories:
        print('Categories remaining: {0}'.format(categories_remaining))
        print('Include {0}'.format(category.category_name))
        category_choice = btc.read_int_ranged('1 to include, 2 to exclude: ', 1, 2)
        if category_choice != 1:
            categories_for_roundup.append(category)
    roundup_title = btc.read_text('Enter the roundup title: ')
    roundup_month = btc.read_int_ranged('Enter roundup month: ', 1, 12)
    roundup_year = btc.read_int_ranged('Enter roundup year: ', 1, 2100)
    filename = btc.read_text('Enter roundup filename: ')
    roundup_choice = btc.read_int_ranged('Enter 1 to export roundup, 2 to cancel: ', 1, 2)
    if roundup_choice == 1:
        for category in categories_for_roundup:
#        for category in roundup_categories:
            category.articles = db.get_articles_for_roundup(roundup_month, roundup_year, category.id)
        roundup_docx.create_complete_roundup(filename=filename, roundup_title=roundup_title, categories=categories_for_roundup)
        #display_title()
    elif roundup_choice == 2:
        print('Roundup export cancelled. Return to main menu.\n')
    

def get_articles_by_category(category=None, start_date=None, end_date=None):
    #print('get_articles_by_category called')
#    print(category.isnumeric())
    #print(start_date)
    #print(end_date)
    if not category:
        category = btc.read_text("Enter category name or number here:  ")
    if not start_date:
        start_date = btc.read_text("Enter starting date: ")
        start_date = parse(start_date)
    if not end_date:
        end_date = btc.read_text("Enter ending date: ")
        end_date = parse(end_date)
    #start_date = parse(start_date)
    #end_date = parse(end_date)
    if category.isalpha() == True:
        print('category name detected')
        display_articles_by_category_name(category_snippet=category,
                                          start_date=start_date,
                                          end_date=end_date)
    elif category.isnumeric() == True:
        print('numeric category ID detected')
        #try:
            #category_id = int(category)
        display_articles_by_category_id(category, start_date=start_date, end_date=end_date)
            
        #except:
            #print('Article search cancelled. Return to main menu.\n')
         


category_menu = ['add_cat - Add a category', 'update_cat - Update category name',
                 'del_cat - delete category', 'cat_help - display categories']

def category_interface(command):
    category_commands = {'add': add_category,
                       'update': update_category,
                       #'display': display_categories,
                       'delete' : delete_category,
                       'stats': get_articles_by_category,
                       }
    
    if not command:
        print('Enter command')
    else:
        try:
            command=category_commands[command]()
        except KeyError:
            print('Invalid suffix for category menu')


def export_interface(command):
    export_commands = {'date': export_roundup_by_date, 'category' : export_roundup_by_category}
    
    if not command:
        print('Enter command')
    else:
        try:
            command=export_commands[command]()
        except KeyError:
            print('Please enter a valid parameter for "export"')


def get_stats(start_date=None, end_date=None):
    #del command
    print('Get stats between two dates')
    if not start_date:
        start_date = btc.read_text('Enter start date: ')
    if not end_date:
        end_date = btc.read_text('Enter end date: ')
    try:
        #start_date = parse(start_date)
        #end_date = parse(end_date)
        get_date_range_category_stats(start_date, end_date)
    except Exception as e:
        print(e)
        return
    
def split_command(command, splitter = ' '):
    #if type(command) != int:
    try:
        split_command = command.split(splitter)
        return split_command[0], split_command[1]
    except Exception as e:
        print(e)
        
def parse_arg(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

def parse_dates(arg):
    'Convert a series of zero or more numbers to an argument tuple of dates'
    try:
        #Let's try to split the argument using space as a separator
        dates = tuple(map(parse, arg.split()))
        dates = [i.date() for i in dates]
        return dates
    except ValueError:
        print('Invalid date format, please enter dates with " " as a separator')
        return
    except TypeError:
        print('Invalid date format')         
        return

class RGenCMD(cmd.Cmd):
        
    intro = "Welcome to RoundupGenerator 3.1"
    prompt = "(RoundupGenerator) "
    entry = ""
           
    def do_search_id(self, command):
        display_article_by_id(command)
        
    def help_search_id(self):
        print('''Enter search_id [article_id] to search for articles by ID.
for example:
search_id 18 will find the article with ID 18''')
        
    def do_id_range(self, command):
        try:
            start_id, end_id=parse_arg(command)
            display_article_by_id_range(start_id, end_id)
        except IndexError:
            print('id_range must be followed by the starting and ending IDs')
            print('"-" must be used to separate the starting and ending dates')
        except ValueError:
            print('id_range only takes integers as arguments')
        
    def help_id_range(self):
        print('enter id_range [starting id]-[ending id]')
        #print('Enter id_range without any arguments')
        print('id_range returns a list of articles with an ID greater than')
        print('the minimum value and less than the maximum value')
        
    def do_search_name(self, command):
        display_articles_by_name(command)
        
    def help_search_name(self):
        print('enter search_name [name snippet] to search by name')
        print('search_name will find all the articles in ')
        
#    def do_search_category(self, command):
#        get_articles_by_category(command)
#        
#    def help_search_category(self):
#        print('Enter search_category [name or id] to find a category')
#        print('Takes either the category name or category ID as input')
            
    def do_search_date(self, command):
        try:
            dates = parse_dates(command)
            if len(dates) == 1:
                search_single_date(dates[0])
            elif len(dates) == 2:
                start_date, end_date = dates[0], dates[1]
                if start_date > end_date:
                    print('start date must come before end date') #starting date must come first
                    return
                search_date_range(start_date, end_date)
        except ValueError as v:
            print(v)
    
    def do_search_category(self, command):
        try:
            value, dates = split_command(command, splitter = '-')
            value = value.lstrip()
            value = value.rstrip()
            start_date, end_date = parse_dates(dates)
            get_articles_by_category(category=value, start_date=start_date,
                                     end_date=end_date)
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
            
    def help_search_category(self):
        print('''
        Prototype advanced category search.
        Enter 'adv_cat_search [id/name] - [start date] [end_date]'
        ''')
    
    def help_search_date(self):
        print('Enter search_date [date] to search for a single date')
        print('e.g.:')
        print('search_date 05/02/2019')
        print('search_date 06/14/2019')
        print('Enter search_date [date_1] [date_2] to search a range of dates')
        
#    def do_search_date_range(self, command):
#        try:
#            start_date, end_date = parse_dates(command)
#            search_date_range(start_date, end_date)
#        except ValueError:
#            print('Date range entered incorrectly, return to main menu.')
#        except TypeError:
#            print('Date range entered incorrectly, return to main menu')
#
#    def help_search_date_range(self):
#        print('Enter search_date_range without any suffix')
#        print('A prompt will appear on screen')
#        print('allowing entry of start and ending dates')
        
    def do_search_author(self, command):
        display_articles_by_author(command)
        
    def help_search_author(self):
        print('Enter search_author [author_name] to find the author')
        
    def do_search_publication(self, command):
        display_articles_by_publication(command)
        
    def help_search_publication(self, command):
        print('Enter search_publication [publication_title]')
        print('Partial titles are acceptable')
        
    def do_search_desc(self, command):
        display_articles_by_description(command)
        
    def help_search_desc(self):
        print('enter search_desc [description snippet] to search by description')
        print('use "search_desc Not Specified" to find undescribed articles')
        
    def do_import_from_csv(self, command):
        del command
        #print('import function temporarily disabled')
        get_csv_in_directory()
    
    def help_import_from_csv(self):
        print('''Import articles from a CSV file. import_from_csv is entered
without any suffix''')
    
    def do_add(self, command):
        Article.add_from_newspaper(link=command)
        #add_article_from_newspaper(link=command)
        
    def help_add(self):
        print('''Enter add [link] to add articles:
add [link] creates an article from [link] using the newspaper module''')
        
    def do_manual_add(self, command):
        manual_add(link=command)
        
    def help_manual_add(self):
        print('''Enter manual_add [link] to add an article manually.
The user will be prompted to enter the article's category. If the category
exists, then the prompts will gather the data for the other attributes.
Invalid categories will cancel article creation. Keyboard interrupts (CTRL+C)
will return to the main menu.
''')
    
    def do_udname(self, command):
        update_article_name(article_id = command)
    
    def help_udname(self):
        print('udname [article_id] updates the name of an article')
        print('example: udname 18 \tupdates article id 18')
        
    def do_udartcat(self, command):
        #We pass the article ID to the other function as a command
        update_article_category(article_id = command)
        
    def help_udartcat(self):
        print('udartcat [article_id] updates the category of an article')
        print('example: udartcat 12 \tupdates the category for article id 12')
        
    def do_udartdesc(self, command):
        update_article_description(article_id=command)
        
    def help_udartdesc(self):
        print('udartdesc [article_id] updates the description of an article')
        print('example: udartcat 13 \t updates the description for article id 13')
        
    def do_udartauth(self, command):
        update_article_author(article_id=command)
        
    def help_udartauth(self):
        print('udartauth [article_id] updates an article\'s author')
        print('Note: this does not affect other articles from the same author')
        
    def do_udartpub(self, command):
        update_article_publication(article_id=command)
        
    def help_udartpub(self):
        print('udartpub [article_id] updates an article\'s publication')
        print('Note: this does not affect other articles from the same publication')

    def do_udartdate(self, command):
        update_article_date(article_id = command)
        
    def help_udartdate(self):
        print('udartdate [article_id] updates the date of an article')
        print('The function calls a prompt for the user to enter the date')
        
    def do_delete_article(self, command):
        delete_article(article_id=command)
        
    def help_delete_article(self):
        print('delete [article_id]')
        print('deletes the selected article from the database')
        print('Note: this is currently irreversible')
        
    def do_categories(self, command):
        category_interface(command)
    
    def help_categories(self):
        print('Opens the category interface')
        print('categories add - add category')
        print('categories update - update category name')
        print('categories display - display categories')
        print('categories delete - delete category')
        print('')
        
    def do_stats(self, command):
        try:
            start_date, end_date = parse_dates(command)
            get_stats(start_date, end_date)
        except ValueError:
            print('Date range entered incorrectly, return to main menu.')
        except TypeError:
            print('Date range entered incorrectly, return to main menu')
    
    def help_stats(self):
        print('stats displays article data for a specified date range')
        print('Enter "stats [starting_date] [ending_date]" to print stats')
        
    def do_category_chart(self, command):
        try:
            start_date, end_date = parse_dates(command)
            get_category_chart(start_date, end_date)
        except Exception as e:
            print(e)
    
    def do_complete_desc(self, command):
        #command = split_command(command)
        try:
            start_date, end_date = parse_dates(command)
        
            finalize_article_descriptions(start_date=start_date, end_date=end_date)
        except TypeError:
            print('complete_desc command entered incorrectly')
        except ValueError:
            print('complete_desc command entered incorrectly')
            
    
    def help_complete_desc(self):
        print('finalize [month], [year]')
        print('finalize 6 2019 : finalizes the June 2019 articles')
        
    def do_export(self, command):
        export_interface(command)
        
    def help_export(self):
        print('''export [option] is used to output the article data into a finished roundup
in a docx file. [option] choices are:
export category - export roundup by category
export month - export roundup by month
export finalize - finalize title stripping
export finish_desc - finish article descriptions''')
        
    def do_display_categories(self, command):
        Category.display_categories(command)
        
    def help_display_categories(self):
        print('Displays a list of the currently available categories.')
        
    def do_exit(self, arg):
        db.close()
        print('Exiting Roundup Generator')
        sys.exit()
        
    def help_exit(self):
        print('Exits the program, closes the database')
        
    def do_quit(self, arg):
        db.close()
        print("Quitting Roundup Generator")
        sys.exit()
        
    def help_quit(self):
        print('Exits the program, closes the database')

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception as e:
            print(e.__class__, ":", e)  
            
def main():
    db.connect()
    app = RGenCMD().cmdloop()
    
if __name__ == '__main__':
    main()
