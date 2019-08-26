# final_roundup
 Finalized verison of roundup

This is a fork of roundup_generator, which is a news scraper designed to build monthly news roundups for jadaliyya.com. This version of the project fixes a major flaw in the first version: separate columns for the day, month, and year for each article.

This application is initialized by opening up the ui.py file in an IDE with the correct dependencies installed.

The Article and Category classes can be found in the objects.py file.

db.py is an old file that is being used to copy/modify code to restore functionality in the new version.

required dependencies:

newspaper
sqlalchemy
BeautifulSoup
tqdm
dateutil
