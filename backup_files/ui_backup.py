#!/usr/bin/env/python3

'''
5/22/19 - Get article titles using BeautifulSoup

'''

import db
from objects import Article, Category
import roundup_docx2 as roundup_docx
import BTCInput2 as btc
import operator
import csv
import glob
import cmd
import sys
import news_article as na
import datetime
import tqdm
from matplotlib import pyplot as plt
from dateutil.parser import parse


'''perhaps create a menu that appears when you choose the edit article option
then gives you choice of what to edit'''

        
def display_menu(title, menu_items, end='   '):
    print(title.upper())
    for i in menu_items:
        print(i, end=end)

def from_newspaper(link):
    '''
    Adds an article from the newspaper module after downloading it
    '''
    for i in tqdm.tqdm(range(1)):
        try:
            newNewsItem = na.get_article_from_url(link)
        except:
            print('Article download failed, invalid URL')
            print('Returning to main menu')
            return
    print(newNewsItem)
    try:
        name = newNewsItem.title #get the title for the article
    except Exception as e:
        print(e)
        name = btc.read_text('Please enter title: ')
        #get article author
    try:
        author = ' '.join(newNewsItem.authors)
        #get article publication
    except Exception as e:
        print(e)
        author = btc.read_text('Please enter author: ')
    try:
        #works for most websites, but not Sudan Tribune
        publication = newNewsItem.meta_data['og']['site_name']
    except Exception as e:
        print(e)
        publication = btc.read_text('Please enter publication: ')
    try:
        year = newNewsItem.publish_date.year
        month = newNewsItem.publish_date.month
        day = newNewsItem.publish_date.day
        new_date = datetime.date(day=day, month=month, year=year)
    except Exception as e:
        print(e)
    #use the new btc.read_date() function to simplify this
    try: 
        new_date = btc.read_date('Enter article date MM/DD/YYYY: ')
        
    except Exception as e:
        print('invalid date', e)
    try:
        summary = newNewsItem.summary
    except Exception as e:
        print(e)
        print('Summary download failed')
        summary = 'Summary not found'
    try:
        keywords = ', '.join(newNewsItem.keywords)
    except Exception as e:
        print(e)
        print('Keyword download failed')
        keywords= 'keywords not found'
    print('TITLE - {0} - AUTHOR {1}'.format(name, author))
    print('DATE - {0} - PUBLICATION {1}'.format(new_date.strftime("%m/%d/%Y"), publication))
    print('KEYWORDS: ', keywords)
    display_categories()
    category_id = btc.read_text("Category ID: ")
    category = db.get_category(category_id)
    if category == None:
        print('There is no category with that ID. article NOT added.\n')
        return
    description_choice = btc.read_text('View article description? y/n: ')
    if description_choice == 'y':
        print('Title: {0}'.format(name))
        print('Summary: {0}'.format(summary))
        print('Keywords: {0}'.format(keywords))
    description = btc.read_text("Description or '.' to cancel: ")
    
    if description == ".":
        return
    else:
        new_article = Article(name=name, date=new_date,
                  category=category, link=link, description=description,
                  author=author, publication=publication)
        display_single_article(article=new_article,
                               title_term = new_article.name)
        confirm_article = btc.read_bool(decision="Finalize the article?",
                                        yes='y', no='n',yes_option='Confirm',
                                        no_option='Cancel')
        #This is the user's last chance to decide if they want to add the article
        if confirm_article == True:
            db.add_article(new_article)    
            print(new_article.name + " was added to database.\n")
        elif confirm_article == False:
            print('Article add cancelled. Return to main menu.')
            

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

class Snippet:
    '''
    The snippet class will communicate with the database, with snippets passed to
    sqlalchemy and then searching for the relevant items in the databse.
    '''
    variables = []
    
    def __init__(self, text):
        self.text=text
        self.variable=None

def from_snippet(snippet=None, snippet_type=None, start_date = None,
                 end_date=None):
    '''
    This function takes a snippet, as well as the snippet type, and retrieves
    a value from the database based on that snippet type. For example, if the
    snippet type is 'name' then it retrieves the article by name. If it is
    description, it retrieves it by description. This function is intended
    to replace many of the functions that retrieve data based on text fields.
    '''
    results = None
    if snippet_type == 'description':
        if (start_date != None) or (end_date != None):
            results = db.get_snippet(snippet, snippet_type=snippet_type)
        else:
            results = db.get_snippet(snippet, snippet_type=snippet_type, 
                                     start_date = start_date,
                                     end_date = end_date)
    elif snippet_type == 'title':
        #print(start_date, end_date)
        if (start_date == None) or (end_date == None):
            results = db.get_snippet(snippet, snippet_type=snippet_type)
        else:
            results = db.get_snippet(snippet, snippet_type=snippet_type, 
                                     start_date = start_date,
                                     end_date = end_date)
    elif snippet_type == 'category':
        if (start_date == None) or (end_date == None):
            results = db.get_snippet(snippet, snippet_type=snippet_type)
        else:
            results = db.get_snippet(snippet, snippet_type=snippet_type, 
                                     start_date = start_date,
                                     end_date = end_date)
    elif snippet_type == 'category_id':
        #print('category id detected')
        if (start_date == None) or (end_date == None):
            #category_id = db.get_category(snippet)
            results = db.get_snippet(snippet, snippet_type=snippet_type)
        else:
            results = db.get_snippet(snippet, snippet_type=snippet_type, 
                                     start_date = start_date,
                                     end_date = end_date) 
        #results = db.get_snippet(snippet, snippet_type='title') #remember it is called name
    if results == None:
        print('There is no article with that {0}.\n'.format(snippet_type))
    else:
        if snippet_type == 'title':
            display_articles(results, str('Results for {0}'.format(snippet)))
        elif snippet_type == 'description':
            display_articles(results, str('Results for {0}'.format(snippet)))
        elif snippet_type == 'category':
            display_articles(results, str('Results for {0}'.format(snippet)))
        elif snippet_type == 'category_id':
            category_id = db.get_category(snippet) #retrieve the category for display
            #this replicates the depricated get_articles_by_category_id function
            category_name = category_id.category_name #get the name to display
            display_articles(results, str('Results for {0}'.format(category_name)))
        else:
            print('Search cancelled, returning to main menu.')
        
 
def search_single_date(article_date):
    assert type(article_date) == datetime.date
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
    category = btc.read_int('Enter category for article: ')
    category = db.get_category(category)
    new_article = Article.manual_add(link=link, category=category)
    db.add_article(new_article)
    print(new_article.title + " was added to database.\n")
    #Article.manual_add(link)



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
            new_date = btc.read_date('Enter new date: ')
            date_choice = btc.read_int_ranged('1 to change date to: {0}, 2 to cancel: '.format(new_date),
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
    #undescribed = db.get_date_range_undescribed_articles(description_snippet='Not specified',
    #                                                     start_date=start_date,
    #                                                     end_date=end_date)
    undescribed = db.get_snippet(snippet='Not specified',
                                 start_date=start_date,
                                 end_date=end_date,
                                 snippet_type='description')
    #We call the get_snippet function with "Not specified" as the description
    #because that's the description for all undescribed articles imported
    #from csv files
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
            db.delete_item(article_id, item_type='article')
            print("'" + article.name + "' was deleted from database.\n")
        else:
            print("'" + article.name + "' was NOT deleted from database.\n")
    except AttributeError as e:
        print(e, 'Article id not found')

def add_category():
    '''
    Planned change: move manual category creation code to the objects.py file
    '''
    new_category = Category.from_input()
    if new_category.category_name != '.':
        db.add_category(new_category)        
        print('New category created: {0}'.format(new_category.name))
    else:
        print('Invalid name, new category not created.')

        
def update_category(category_id=0):
    if category_id == 0:
        category_id = int(input("category ID: "))
    category = db.get_category(category_id)
    #articles = db.get_articles_by_category_id(category_id)
    #display_articles(articles, category.category_name.upper())
    print('Current category name: {0}'.format(category.category_name))
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
        delete_choice = btc.read_bool(decision='Are you sure?',
                                      yes='1', no='2', yes_option='delete', no_option='cancel')
        if delete_choice == True:
            db.delete_item(item_id=category_id, item_type='category')
        else:
            print('Delete cancelled, returning to category menu')
        
def export_roundup_by_date():
    roundup_title = btc.read_text('Enter the roundup title: ')
    start_date = btc.read_date('Enter the starting date: ')
    end_date = btc.read_date('Enter the ending date: ')
    print('start date: ', start_date, 'end date: ', end_date)
    print('start date type:', type(start_date), 'end date type:', type(end_date))
    filename = btc.read_text('Enter roundup filename: ')
    roundup_choice = btc.read_int_ranged('Enter 1 to export roundup, 2 to cancel: ', 1, 2)
    if roundup_choice == 1:
        roundup_categories = db.get_categories() #We get the articles by
        #category to sort them by category
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
    display_categories()
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
    if not category:
        category = btc.read_text("Enter category name or number here:  ")
    if not start_date:
        start_date = btc.read_date("Enter starting date: ")
        #start_date = parse(start_date)
    if not end_date:
        end_date = btc.read_date("Enter ending date: ")
    if category.isalpha() == True:
        from_snippet(snippet=category, start_date=start_date,
                    end_date=end_date, snippet_type='category')
        
    elif category.isnumeric() == True:
        from_snippet(snippet=category, start_date=start_date,
                     end_date=end_date, snippet_type='category_id')    
        #except:
            #print('Article search cancelled. Return to main menu.\n')

def category_interface(command):
    category_commands = {'add': add_category,
                       'update': update_category,
                       'display': display_categories,
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
    
def display_categories(command=''):
        del command
        print("CATEGORIES")
        categories = db.get_categories()  
        for category in categories:
            print(str(category.CategoryID) + ". " + category.category_name.strip(), end='   ')
        print()
    
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
        
    intro = "Welcome to RoundupGenerator 3.2"
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
        #from_snippet(snippet=command, snippet_type = 'title')
        #display_articles_by_name(command)
        try:
            snippet, dates = split_command(command, splitter = '-')
            snippet = snippet.lstrip()
            snippet = snippet.rstrip()
            #print(snippet)
            start_date, end_date = parse_dates(dates)
            #print(start_date, type(start_date))
            #print(end_date, type(end_date))
            from_snippet(snippet=snippet, start_date=start_date,
                                     end_date=end_date, snippet_type='title')
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
        
    def help_search_name(self):
        print('enter search_name [name snippet] - [start_date] [end_date] to search by name')
        print('For example:')
        print('search_name somalia - 08/01/2019 08/31/2019')
            
    def do_search_date(self, command):
        try:
            dates = parse_dates(command)
            if len(dates) == 1:
                search_single_date(dates[0])
            elif len(dates) == 2:
                start_date, end_date = dates[0], dates[1]
                print(start_date, end_date)
                if start_date > end_date:
                    print('start date must come before end date') #starting date must come first
                    return
                search_date_range(start_date, end_date)
        except ValueError as v:
            print(v)
        except TypeError as t:
            print(t, 'Invalid date entered')
            
    def help_search_date(self):
        print('Enter search_date [date] to search for a single date')
        print('e.g.:')
        print('search_date 05/02/2019')
        print('search_date 06/14/2019')
        print('Enter search_date [date_1] [date_2] to search a range of dates')
    
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
        #I think the code block below this will be the initial functionality of what the
        #new entryParser class does
        try:
            snippet, dates = split_command(command, splitter = '-')
            snippet = snippet.lstrip()
            snippet = snippet.rstrip()
            #print(snippet)
            start_date, end_date = parse_dates(dates)
            #print(start_date, type(start_date))
            #print(end_date, type(end_date))
            from_snippet(snippet=snippet, start_date=start_date,
                                     end_date=end_date, snippet_type='description')
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
        
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
        from_newspaper(link=command)
        #Article.add_from_newspaper(link=command)
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
        start_date, end_date = parse_dates(command)
    
        finalize_article_descriptions(start_date=start_date, end_date=end_date)
            
    
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
