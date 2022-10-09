from ctypes import sizeof
from types import NoneType
from wsgiref import headers
import requests
from bs4 import BeautifulSoup
import pandas
from email.message import EmailMessage
from time import sleep
import ssl
import smtplib
import re
from selenium import webdriver
import json

ProductData = []

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
BASE_URL = "https://www.amazon.de/hz/wishlist/ls/2Z4QOT63YGLGF"
ITEM_URL = "https://www.amazon.de/hz/wishlist/slv/items?filter=unpurchased&paginationToken=eyJGcm9tVVVJRCI6IjBmMzZmMTg1LWJkMmMtNDk3Zi1hZDEyLWE1MTRjOTVkYWUxYiIsIlRvVVVJRCI6ImJlY2Y0ZThkLWMxOWQtNDMzMy1hMjgyLTE4MjA4MDU4ZDA0MCIsIkVkZ2VSYW5rIjoxMjU1NjgzfQ&itemsLayout=LIST&sort=default&type=wishlist&lid=2Z4QOT63YGLGF&ajax=true"

#page = requests.get(BASE_URL,headers=HEADERS)
page = requests.get(ITEM_URL,headers=HEADERS)



soup = BeautifulSoup(page.content, features="html.parser")
pageinationToken = "https://www.amazon.de" + json.loads(soup.find("script").string)['showMoreUrl']
lastToken = "https://www.amazon.de/hz/wishlist/slv/items?filter=unpurchased&paginationToken=&itemsLayout=LIST&sort=default&type=wishlist&lid=2Z4QOT63YGLGF"

loopcounter = 0

tag = soup.find(id=re.compile("itemName"))

print(tag.get("href"))

def method():
    while(pageinationToken != "https://www.amazon.de" and "paginationToken=&itemsLayout" not in pageinationToken):
        subsequentPage = requests.get(pageinationToken,headers=HEADERS)
        subsequentSoup = BeautifulSoup(subsequentPage.content,features="html.parser")
        pageinationToken = "https://www.amazon.de" + json.loads(subsequentSoup.find("script").string)['showMoreUrl']
        soup.extend(subsequentSoup)
        print("GET: " + str(loopcounter))
        print(pageinationToken)
        loopcounter = loopcounter + 1 
        itemcount = len(soup.findAll("li"))
        print(itemcount)


    for items in soup.findAll("li"):
        itemname = items.find(id=re.compile("itemName.*"))
        if itemname is not None:
            print(itemname.text)
            print("-------------")
