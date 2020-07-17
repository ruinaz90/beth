#! python3

# COMMENTS
# second web scraper i built after completing automate the boring stuff
# chatting to Semolina made me think with a tad more effort this could be made into something useful, though the copyright could be an issue.
# could also be a nice project.

# machine called Beth after author on site.
# runs ok, some bugs:
    # not all recipe description is scraped, particularly in multistep recipes. needs attention to html
    # failure on some recipes leaving multiple sheets blank. think that could be fixed in how we find the url
    # only logs one section. perhaps a loop with different myurl.


import bs4, re, logging
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from datetime import date
import xlsxwriter, winsound

print('starting')
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

#get the url first, and count how many recipes you want to scrape
myurl = 'https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/' #gets url
req = Request(myurl, headers={'User-Agent': 'Mozilla/5.0'})#starts connection
webpage = urlopen(req).read()#gets info
pageSoup = soup(webpage, "html.parser") #parses html 

recipes = pageSoup.findAll("div",{"class":"archive-post"}) #finds all recipes

filename = "BB.xlsx"
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet()
num = 1

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

for r in recipes: #for each recipe, navigate to the list and download the ingredients [later instructions]
    try:
        xtitle = r.a["title"]
        print(xtitle)
        title = xtitle.replace(" ", "-")
        url = "https://www.budgetbytes.com//"+ title
        
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})#starts connection
        webpage = urlopen(req).read()#gets info
        pageSoup = soup(webpage, "html.parser") #parses html  

        r= pageSoup.find('div', {"id":"content"})
        ingreds = r.find("ul", "wprm-recipe-ingredients")
        steps = pageSoup.findAll("div", {"class":"wprm-recipe-instruction-text"})

        h = 0
        xtitle = xtitle[0:25]
        bold = workbook.add_format({'bold': True}) # make bold option
        worksheet = workbook.add_worksheet(xtitle) #make new sheet
        row = 0
        worksheet.write(row, col,     xtitle, bold)
        row = row + 1
        worksheet.write(row, col,     url)
        row = row + 2
        worksheet.write(row, col, "Ingredients", bold)
        for i in ingreds:
            icopy = i.text
            bpos = icopy.find('(')
            icopy = icopy[0:bpos]
            
            worksheet.write(row, col, icopy)
            row = row + 1
        row += 1
        worksheet.write(row, col, "Steps", bold)
        for s in steps:
            worksheet.write(row, col,     s.text)
            row = row + 1
        h += 1
        num += 1

    #if there'  problem, plug the supected url into google and select the first result.
    except:
        try:
            logging.error('ERROR WITH ' + url) 
            from googlesearch import search 
            # to search 
            for newurl in search(url, tld='com', lang='en', num=1, start=0, stop=1, pause=2.0):
                print(newurl) 

            req = Request(newurl, headers={'User-Agent': 'Mozilla/5.0'})#starts connection
            webpage = urlopen(req).read()#gets info
            pageSoup = soup(webpage, "html.parser") #parses html  

            r= pageSoup.find('div', {"id":"content"})

            ingreds = r.find("ul", "wprm-recipe-ingredients")
            
            print(title)
            print(url)
            for i in ingreds:
                print(i.text)
            print('-'*30)

            logging.error('ERROR RESOLVED WITH ' + newurl)
        except:
            logging.error('ERROR CANNOT BE SOLVED WITH ' + title) 
            pass

workbook.close()
print('not starting')