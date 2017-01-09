from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re

# Function for getting data
def getPSstoredata(link):
    # Start the webdriver and load the page
    driver = webdriver.Chrome()
    driver.get(link)
    # Wait for the dynamically loaded price element to show up
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "buyPrice")))
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
    data = pd.DataFrame({'titles':titles, 'prices':prices})
    driver.close()
    return data

def main():
    # Grab the data for the first 100 titles
    firstpage = getPSstoredata("https://store.playstation.com/#!/en-us/top-games/cid=STORE-MSF77008-TOPGAMES")
    secondpage = getPSstoredata("https://store.playstation.com/#!/en-us/top-games/cid=STORE-MSF77008-TOPGAMES/2")
    thirdpage = getPSstoredata("https://store.playstation.com/#!/en-us/top-games/cid=STORE-MSF77008-TOPGAMES/3")
    fourthpage = getPSstoredata("https://store.playstation.com/#!/en-us/top-games/cid=STORE-MSF77008-TOPGAMES/4")
    # Merge the dataframes
    dailybuild = firstpage.append(secondpage, ignore_index=True).append(thirdpage, ignore_index=True).append(fourthpage,ignore_index=True)
    # Add the date of data collection
    dailybuild['Date'] = time.strftime("%m/%d/%y")
    # Add the rank of the game on that date
    dailybuild['Rank'] = range(1, len(dailybuild['Date'])+1)
    dailybuild['titles'] = dailybuild['titles'].astype(str)
    dailybuild['prices'] = dailybuild['prices'].astype(str)
    # Scrub the output on non-ASCII symbols and text using regular expressions
    for title in range(0, len(dailybuild['titles'])):
        dailybuild['titles'][title] = re.sub(r'[\\]...', '', dailybuild['titles'][title])
        dailybuild['titles'][title] = dailybuild['titles'][title][:-1]
        dailybuild['titles'][title] = dailybuild['titles'][title][2:]
        dailybuild['prices'][title] = dailybuild['prices'][title][:-1]
        dailybuild['prices'][title] = dailybuild['prices'][title][3:]
    with open('playstationstore.csv', mode='a') as f:
        dailybuild.to_csv(f, header=False)

main()



