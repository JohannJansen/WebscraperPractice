
import string
import requests
from time import sleep
import re
import time
from bs4 import BeautifulSoup
import json
import ssl
import smtplib
from email.message import EmailMessage
from datetime import datetime
import random

ProductData = []

#!!!These fields need to be filled in with the login data for a gmail acc and a recieving email!!!
email_sender = ''
email_pw = ''
email_reciever = ''

user_agents = [
  "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
  "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
  "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
  ]

random_user_agent = random.choice(user_agents)

HEADERS = ({
    'User-Agent': random_user_agent
    })
BASE_URL = "https://www.amazon.de/hz/wishlist/ls/7J62CKP25KAM"
ITEM_URL = "" #searched for automatically


def findListURL():
    page = requests.get(BASE_URL,headers=HEADERS)
    soup = BeautifulSoup(page.content, features="html.parser")
    itemurl = "https://www.amazon.de" + json.loads(soup.find("script",string=re.compile("showMoreUrl")).string)['showMoreUrl']
    return itemurl



def manageProductdata(Data,updateflag):

    page = requests.get(ITEM_URL,headers=HEADERS)
    soup = BeautifulSoup(page.content, features="html.parser")
    initialToken = json.loads(soup.find("script",string=re.compile("showMoreUrl")).string)['showMoreUrl']
    if initialToken is None:
            print("Unable to read Token. The results of this check dont include any products")
            return
    pageinationToken = "https://www.amazon.de" + initialToken
    currentIndex = 0

    while(pageinationToken != "https://www.amazon.de" and "paginationToken=&itemsLayout" not in pageinationToken):
        subsequentPage = requests.get(pageinationToken,headers=HEADERS)
        subsequentSoup = BeautifulSoup(subsequentPage.content,features="html.parser")
        token = json.loads(subsequentSoup.find("script",string=re.compile("showMoreUrl")).string)['showMoreUrl']
        if token is None:
            print("Unable to read Token. The results of this check might not include all products")
            return
        pageinationToken = "https://www.amazon.de" + token
        soup.extend(subsequentSoup)
        

    changeditems = []

    for items in soup.find_all("li"):
        itemname = items.find(id=re.compile("itemName.*"))
        used_and_new = items.find(id=re.compile("used-and-new.*"))
        itemlink = "https://www.amazon.de" + soup.find(id=re.compile("itemName")).get("href")
    
        if itemname is not None:
            number_used_and_new = int(re.sub('[^0-9]','',used_and_new.text)) if used_and_new is not None else 0
            text_itemname = itemname.text.strip()
            if updateflag:
                if number_used_and_new is Data[currentIndex][1]:
                    currentIndex+=1
                elif number_used_and_new < Data[currentIndex][1]:
                    Data[currentIndex] = (text_itemname,number_used_and_new,itemlink)
                    currentIndex+=1
                elif number_used_and_new > Data[currentIndex][1]:
                    changeditems.append(currentIndex)
                    Data[currentIndex] = (Data[currentIndex][0],number_used_and_new,Data[currentIndex][2])
                    currentIndex+=1
            else:
                Data.append((text_itemname,number_used_and_new,itemlink))
    print("no changes to the previous List" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    notify(changeditems)

def notify(changeditems):
    if len(changeditems) == 0:
        return

    print("notify called with more than 0 items")
    
    subject = "Amazon procuts back in stock"
    emailText = "The following products are back in Stock \n"

    for i in changeditems:
        emailText += ProductData[i][0] + " can be found at: " + ProductData[i][2] + "\n"
    
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciever
    em['subject'] = subject
    em.set_content(emailText)
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(email_sender,email_pw)
        smtp.sendmail(email_sender,email_reciever,em.as_string())


ITEM_URL = findListURL()
manageProductdata(ProductData,False)
print(ProductData)
while True:
    manageProductdata(ProductData,True)
    sleep(30)



