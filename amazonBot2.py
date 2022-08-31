from types import NoneType
from wsgiref import headers
import requests
from bs4 import BeautifulSoup
import pandas
from email.message import EmailMessage
from time import sleep
import ssl
import smtplib

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
BASE_URL = "http://amazon.de/dp/"

#!!!These fields need to be filled in with the login data for a gmail acc and a recieving email!!!
email_sender = 'yoshi081200@gmail.com'
email_pw = 'epdeayzljqwgjwfr'
email_reciever = 'jj00@web.de'

#Reads the given Data from the products.csv and adds a condition met column in the Dataframe
def setup_csv_data():
    read_data = pandas.read_csv('products.csv', sep=';')
    isConditionMet = []
    for x in range(len(read_data)):
        isConditionMet.append(False)
    read_data['isConditionMet'] = isConditionMet
    return read_data

def product_checker(product_data):
    for x, index in enumerate(product_data.index):
        current_asin = product_data.asin[index]
        current_page = requests.get(BASE_URL + current_asin,headers=HEADERS)
        soup = BeautifulSoup(current_page.content, features="html.parser")

        conditionMet = False

        match product_data.condition[index]:
            case "availability":
                conditionMet = check_availability(soup)
            case "price":
                conditionMet = check_price(soup,product_data.value[index])
            case _:
                print()
                #nothing

        product_data.isConditionMet[index] = conditionMet
    return product_data

def check_availability(soup):
    tag = soup.find(id='availability')
    if tag is not None:
        availability = tag.get_text().strip()
        if availability == "In stock.":
            return True
    return False

def check_price(soup,price):
    tag = soup.find(id="corePrice_feature_div")
    
    if tag is not None:
        product_price = tag.get_text().strip().strip("€").split(",")[0]
        print(product_price)
        if int(product_price) <= price:
            return True
    return False

def condition_notify(product_csv_data):
    didarticleUpdate = False
    subject = "Amazon products are back in stock"
    emailText = "Hello User of this very professional webscraping tool. Out of the selected products the following were found to be available again: \n"
    for x, index in enumerate(product_csv_data.index):
        if product_csv_data.isConditionMet[index] == True:
            didarticleUpdate = True
            emailText += product_csv_data.name[index] + " you can find the product usign the following link: " + BASE_URL + product_csv_data.asin[index] + "\n"
            product_csv_data = product_csv_data.drop(index=x)

    if didarticleUpdate:
        #print(emailText)
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_reciever
        em['subject'] = subject
        em.set_content(emailText)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,email_pw)
            smtp.sendmail(email_sender,email_reciever,em.as_string())

    return product_csv_data


csv_data = setup_csv_data()
while True:
    csv_data = product_checker(csv_data)
    csv_data = condition_notify(csv_data)
    sleep(60)