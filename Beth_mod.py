#! python3
"""
Beth_mod.py - Based on the Beth.py file

Program currently does the following:
    # Pulls recipe titles
    # Creates URL based on recipe titles
    # Creates Excel file with recipe names for worksheets

[recipes] list = recipe names
[recipe_urls] list = links to recipes
"""

import logging
import xlsxwriter
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug("Program start")
recipes, recipe_url_titles, recipe_urls = [], [], []

logging.debug("Connect to page")
page_url = 'https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/'
req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})  # Start connection
recipes_page = urlopen(req).read()  # Get info
soup = BeautifulSoup(recipes_page, 'html.parser')  # Parse HTML

logging.debug("Recipe loop")
# Get recipe titles
recipe_titles = soup.findAll('h2', attrs={'class': 'post-title'})
for recipe_title in recipe_titles:
    # Recipe name
    recipe_name = recipe_title.text.strip()
    recipes.append(recipe_name.replace('’', '\''))  # Fix apostrophe

    # Recipe URL name
    recipe_lowercase = recipe_name.replace(" ", "-").lower()
    recipe_url_titles.append(recipe_lowercase.replace('’', ''))

logging.debug("Recipe link loop")
# Get recipe links
for recipe_url_title in recipe_url_titles:
    url = 'https://www.budgetbytes.com/' + recipe_url_title
    recipe_urls.append(url)

logging.debug(f"var recipes: {recipes}")
logging.debug(f"var recipe_urls: {recipe_urls}")

# Create Excel file
workbook = xlsxwriter.Workbook('BB.xlsx')

# Create sheets with recipe names
logging.debug("Worksheet loop")
for recipe in recipes:
    if ':' in recipe:  # Remove colon
        worksheet = workbook.add_worksheet(recipe[:30].replace(':', ''))
    else:
        worksheet = workbook.add_worksheet(recipe[:30])

workbook.close()
logging.debug("Program end")
