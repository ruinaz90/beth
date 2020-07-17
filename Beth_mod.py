#! python3

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

import pandas as pd
import requests, bs4

logging.debug("Start of program")

response = requests.get('https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/')
response.raise_for_status()
bs_object = bs4.BeautifulSoup(response.text, 'html.parser')
type(bs_object)