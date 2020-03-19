########################################################
#################### IMPORT ############################
########################################################
import bs4
from selenium import webdriver
import re
import math
# import numpy
# import pandas as pd
# import re
# import requests
# import datetime
# import time

# Ersetzungen definieren
substitutions = {"1-30": "", "von": " ", "Ergebnissen": "", " ": ""}

def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

###################################################
#################### ARGUMENTS ####################
###################################################

print ('Schon wieder ne Aufgabe für mich?' + '\n' + 'Na gut, ich crawl mal nach: ')
Url = 'https://berufenet.arbeitsagentur.de/berufenet/faces/index?path=null/sucheAZ&let=A'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36','referer': 'https://www.google.de/'}

# Webbrowser starten
Browser = webdriver.Chrome("C:\\Users\\BenediktRunschkeWifO\\\OneDrive - WifOR\\Desktop\\chromedriver.exe")

Browser.get(Url)
Html = Browser.page_source
Soup = bs4.BeautifulSoup(Html, 'lxml')

# Gesamtanzahl der Einträge
NoOfEntries = Soup.findAll(class_="bapf-accessible-table-filter-ergebnisse")
NoOfEntries = NoOfEntries[0]
NoOfEntries = NoOfEntries.contents
NoOfEntries = NoOfEntries[0]
NoOfEntries = replace(NoOfEntries, substitutions)
NoOfEntries = NoOfEntries.strip()

noOfPages = int(math.ceil(int(NoOfEntries) / 30))
