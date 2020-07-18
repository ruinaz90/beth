#! python3
"""
Beth_mod.py - Modified original Beth.py file

Program currently does the following:
    # Pulls recipe titles and URL
    # Creates Excel file with recipe names for worksheets
"""

import logging
import xlsxwriter
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)

logging.debug("Program start")
recipe_dict = {}
recipe_urls = []

# Connect to site
logging.debug("Connect to page")
page_url = 'https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/'
req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
recipes_page = urlopen(req).read()
soup = BeautifulSoup(recipes_page, 'html.parser')

# Get recipe titles
logging.debug("Recipe loop")
recipe_titles = soup.findAll('h2', {'class': 'post-title'})
recipe_url_div = soup.findAll('div', {'class': 'post-image'})
for div in recipe_url_div:
    recipe_urls.append(div.find('a')['href'])

for recipe_title, recipe_url in zip(recipe_titles, recipe_urls):
    # Format recipe name
    recipe_name = recipe_title.text.strip()
    recipe_name = recipe_name.replace('’', '\'')

    # Add name and URL to recipe_dict
    recipe_dict[recipe_name] = recipe_url

logging.debug(f"recipe_dict: {recipe_dict}")

# Create sheets with recipe names
logging.debug("Worksheet loop")
workbook = xlsxwriter.Workbook('BB.xlsx')
for recipe_title, recipe_url in recipe_dict.items():
    worksheet = workbook.add_worksheet(recipe_title[:30].replace(':', ''))
    req = Request(recipe_url, headers={'User-Agent': 'Mozilla/5.0'})
    recipe_page = urlopen(req).read()
    soup = BeautifulSoup(recipe_page, 'html.parser')

    recipe = soup.find('div', {'id': 'content'})
    row = 0
    col = 0

    bold = workbook.add_format({'bold': True})
    worksheet.write(row, col, recipe_title, bold)
    row += 1
    worksheet.write(row, col, recipe_url)

workbook.close()
logging.debug("Program end")
