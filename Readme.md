# Hot Nigeria Jobs Webscraper

[![Downloads](https://pepy.tech/badge/Joblist)](http://www.hotnigerianjobs.com/)

<a href="http://www.hotnigerianjobs.com/" target="_blank">Hot Nigeria Jobs</a> is one of the Nigeria's largest job websites, hosting thousands of job posts for companies.

<code>Joblist.py</code> is a simple Python interface to scrape accounting job posts from the website and prepare them in a Pandas dataframe for analysis.

## Project Title
Web Scraper

### Table of contents
General info
Technologies
Setup
Usage
General info
This project is a Python-based web scraper that can extract job information from a job listing website.

### Technologies
This project is created with:

Python 3.7
requests 2.25.1
BeautifulSoup 4.9.3
pandas 1.2.4

### To run this project, install it locally using pip:

$ pip install requests
$ pip install beautifulsoup4
$ pip install pandas

### Usage
To run this project, follow these steps:

### Import the necessary libraries:

import requests
from bs4 import BeautifulSoup
import pandas as pd

### Load the web_scraper function:

def web_scraper(url):
    ...
    return data
    
### Call the function by passing the URL of the job listing website:

url = 'https://example.com'
data = web_scraper(url)

The function will extract job information from the website and return a pandas dataframe with the following columns: Title, Link, Location, Year, Content, and Job Information.

