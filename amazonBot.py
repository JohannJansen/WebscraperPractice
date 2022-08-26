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

#!!!These fields need to be filled in with the login data for a gmail acc and a recieving email!!!
email_sender = ''
email_pw = ''
email_reciever = ''

#Reads the given URLs and Product names from the csv File and adds another column to track the availability
def setup_csv_data():
    read_data = pandas.read_csv('products.csv', sep=';')
    availabilityBools = []
    for x in range(len(read_data)):
        availabilityBools.append(False)
    read_data['availability'] = availabilityBools
    return read_data

#Checks whether the specified products are currently listed as available on amazon
def product_availability_check(product_csv_data):
    for x, index in enumerate(product_csv_data.index):
        url = product_csv_data.url[index]
        name = product_csv_data.name[index]
        current_page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(current_page.content, features="html.parser")
        tag = soup.find(id='availability')
        if tag is not None: 
            availability = tag.get_text().strip()

            #print("current article: " + name)
            #print("availability for the above URL: " + availability)

            if availability == "In stock." and product_csv_data.availability[index] == False: 
                product_csv_data.availability[index] = True
                #print("article is back in stock!")
        else: 
            print("no information about availibility is given for the specified article")
    return product_csv_data

#Goes through the given data and notifies the user of every available product. The available products are then removed from the list of articles to be checked
def availability_notify(product_csv_data):
    didarticleUpdate = False
    subject = "Amazon products are back in stock"
    emailText = "Hello User of this very professional webscraping tool. Out of the selected products the following were found to be available again: \n"
    for x, index in enumerate(product_csv_data.index):
        if product_csv_data.availability[index] == True:
            didarticleUpdate = True
            emailText += product_csv_data.name[index] + " you can find the product usign the following link: " + product_csv_data.url[index] + "\n"
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
    csv_data = product_availability_check(csv_data)
    csv_data = availability_notify(csv_data)
    sleep(30)

