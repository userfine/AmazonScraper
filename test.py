import mechanize
import urllib2
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import NoSuchAttributeException
from selenium.webdriver.common.keys import Keys
import os
import re

#storelinks = ['https://store.playstation.com/#!/en-us/top-games/cid=STORE-MSF77008-TOPGAMES','https://store.playstation.com/#!/en-us/top-games/cid=STORE-MSF77008-TOPGAMES/2','https://store.playstation.com/#!/en-us/top-games/cid=STORE-MSF77008-TOPGAMES/3','https://store.playstation.com/#!/en-us/top-games/cid=STORE-MSF77008-TOPGAMES/4']

# Start the webdriver and load the page
driver = webdriver.Chrome()
driver.get("https://store.playstation.com/#!/en-us/top-games/cid=STORE-MSF77008-TOPGAMES")

# Wait for the dynamically loaded elements to show up
WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "buyPrice")))

# Grab the data by class name
gametitles = driver.find_elements_by_class_name("cellTitle")
gameprices = driver.find_elements_by_class_name('buyPrice')
gametypes = driver.find_elements_by_class_name('type')

# Initiate the data arrays
titles = []
prices = []
types = []

# loop out the data from the Selenium webelements
for game in gametitles:
    titles.append(game.text.encode('utf-8'))
for game in gameprices:
    prices.append(game.text.encode('utf-8'))
for game in gametypes:
    types.append(game.text.encode('utf-8'))

data = pd.DataFrame({'titles':titles, 'prices':prices}, columns=['Title','Price'])

# Pass to BeautifulSoup
soup = BeautifulSoup(html,'lxml')

for tag in soup.findAll('h3',{'class':'cellTitle'}):
    print (tag.text.encode('utf-8'))


for link in storelinks:
    #browser.get(storelinks[link])
    gametitles = driver.find_elements_by_class_name("cellTitle")
    gameprice = driver.find_elements_by_class_name('buyPrice')
    gametype = driver.find_elements_by_class_name('type')
for game in gametitles:
    print (game.text.encode("UTF-8"))
    print (game.text.encode("UTF-8"))
    print(game.text.encode("UTF-8"))
