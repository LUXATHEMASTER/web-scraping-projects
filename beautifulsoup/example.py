"""
Web Scraping with Beautiful Soup
http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html
"""
from bs4 import BeautifulSoup
import urllib

### Creating a beautiful soup object from a website
r = urllib.urlopen('http://www.aflcio.org/Legislation-and-Politics/Legislative-Alerts').read()
soup = BeautifulSoup(r, "lxml")
print type(soup)

### print few contents from the soup
print soup.prettify()[0:1000]
print 
### Find all div
letters = soup.find_all("div", class_="ec_statements")
print letters[0]
print 

### Print links and text between <a href> and </a>
for i in range(5):
	print letters[i].a["href"]
	print letters[i].a.get_text()
print

### find specific id
print letters[0].find(id="legalert_date")
print letters[0].find(id="legalert_date").get_text()
print

### Writing to file
import os, csv

# Change the directory
os.chdir("C:/")

# with open blahblahblah if you want to write data to file.