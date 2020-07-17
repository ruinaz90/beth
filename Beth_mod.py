#! python3

import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug("Start of program")

recipes, recipe_url_titles, recipe_urls = [], [], []
intab = " -"
outtab = "-"

page_url = 'https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/'
req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})  # Start connection
recipes_page = urlopen(req).read()  # Get info
soup = BeautifulSoup(recipes_page, 'html.parser')  # Parse HTML

# Get recipe titles
recipe_titles = soup.findAll('h2', {'class': 'post-title'})
for recipe_title in recipe_titles:
    # Recipe name
    recipe_name = recipe_title.text.strip()
    recipes.append(recipe_name)

    # Recipe URL name
    recipe_lowercase = recipe_name.replace(" ", "-").lower()
    recipe_url_titles.append(recipe_lowercase.replace('’', ''))

# Get recipe links
for recipe_url_title in recipe_url_titles:
    url = 'https://www.budgetbytes.com/' + recipe_url_title
    recipe_urls.append(url)