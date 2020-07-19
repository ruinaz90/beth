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
urls = [
    'https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/',
    'https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/breakfast-meal-prep/',
    "https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/chicken-meal-prep/",
    "https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/no-re-heat/",
    "https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/vegetarian-meal-prep/"
]
BB_name = ['Budget Friendly Meal Prep', 'Breakfast Meal Prep', 'Chicken Meal Prep', 'No Reheat', 'Vegetarian Meal Prep']

for i in range(len(urls)):

    # Connect to site
    logging.debug("Connect to page, for " + BB_name[i])
    page_url = urls[i]
    req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
    recipes_page = urlopen(req).read()
    soup = BeautifulSoup(recipes_page, 'html.parser')

    # Get recipe titles and URL
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

    # Write to Excel file
    logging.debug("Excel loop")
    workbook = xlsxwriter.Workbook('BB_' + BB_name[i] + '.xlsx')

    for recipe_title, recipe_url in recipe_dict.items():
        ingredients_list = []
        steps_list = []

        # Create sheets with recipe names (up to 30 characters, remove colon from name)
        worksheet = workbook.add_worksheet(recipe_title[:30].replace(':', ''))

        # Connect to recipe page
        req = Request(recipe_url, headers={'User-Agent': 'Mozilla/5.0'})
        recipe_page = urlopen(req).read()
        soup = BeautifulSoup(recipe_page, 'html.parser')

        # Get ingredients
        ingredients = soup.findAll('li', {'class': 'wprm-recipe-ingredient'})
        for ingredient in ingredients:
            ingredients_list.append(ingredient.text.strip())

        # Get steps
        steps = soup.findAll('li', {'class': 'wprm-recipe-instruction'})

        for index, step in enumerate(steps):
            steps_list.append(f"{index + 1}. {step.text.strip()}")

        # Add recipe title and URL to sheet
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', recipe_title, bold)
        worksheet.write('A2', recipe_url)

        # Add ingredients to sheet
        row = 2
        for ingredient in ingredients_list:
            row += 1
            worksheet.write(row, 0, ingredient)

        # Add steps to sheet
        row = 3 + len(ingredients_list) + 1
        for step in steps_list:
            row += 1
            worksheet.write(row, 0, step)

    workbook.close()
logging.debug("Program end")
