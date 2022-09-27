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

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
BASE_URL = "https://www.amazon.de/hz/wishlist/ls/2Z4QOT63YGLGF"

page = requests.get(BASE_URL,headers=HEADERS).scroll
soup = BeautifulSoup(page.content, features="html.parser")
#print(soup.prettify())
itemlist = soup.find("ul",id="g-items")
for items in itemlist.findAll("li"):
    itemname = items.find(id=re.compile("itemName.*"))
    if itemname is not None:
        print(itemname.text)
    print("-------------")
