from lib2to3.pgen2.token import EQUAL
from types import NoneType
from wsgiref import headers
import requests
import pandas
from time import sleep
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

ProductData = []

def manageProductdata(Data,updateflag):
    browser = webdriver.Chrome('D:\Python\chromedriver')
    currentIndex = 0

    browser.get("https://www.amazon.de/hz/wishlist/ls/2Z4QOT63YGLGF")
    time.sleep(1)

    html = browser.find_element(By.TAG_NAME,"body")
    for x in range(100):
        html.send_keys(Keys.DOWN)
        time.sleep(0.1)

    soup = BeautifulSoup(browser.page_source, features="html.parser")
    itemlist = soup.find("ul",id="g-items")
    allItems = itemlist.findAll("li")
    allItemsLength = len(allItems)
    for items in allItems:
        if currentIndex > allItemsLength:
            break
        itemname = items.find(id=re.compile("itemName.*"))
        used_and_new = items.find(id=re.compile("used-and-new.*"))
    
        if itemname is not None:
            number_used_and_new = int(re.sub('[^0-9]','',used_and_new.text)) if used_and_new is not None else 0
            text_itemname = itemname.text.strip()
            if updateflag:
                if number_used_and_new is Data[currentIndex][1]:
                    currentIndex+=1
                elif number_used_and_new < Data[currentIndex][1]:
                    Data.remove(currentIndex)
                    Data.insert((text_itemname,number_used_and_new))
                    currentIndex+=1
                elif number_used_and_new > Data[currentIndex][1]:
                    print("coole Sachen machen")
                    currentIndex+=1
            else:
                Data.append((text_itemname,number_used_and_new))

manageProductdata(ProductData,False)
print(ProductData)
while True:
    manageProductdata(ProductData,True)



