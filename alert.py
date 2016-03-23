#!/usr/bin/python
import time
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lxml import html
import ConfigParser

# config = ConfigParser.RawConfigParser()
# config.read("creds")
# # email_user = config.get('email','user')
# # email_pass = config.get('email','pass')


# Change these values to your desired sale page (the selector and price check were tested on Amazon).
BASE_URL = "https://in.bookmyshow.com/buytickets/"
SMTP_URL = "smtp.gmail.com:587"
XPATH_SELECTOR = '/html/body/section/div/div/ul/li/div/div/div/a/strong/text()'
# XPATH_SELECTOR = '/html/body/section/div/div/ul/li/div/div/div/a/strong'
SLEEP_INTERVAL = 10
#ITEMS is a list of lists, storing ASINs and their maximum prices
# ITEMS = ['batman-v-superman-dawn-of-justice-imax-3d-bengaluru/movie-bang-ET00038215-MT/20160324', 'batman-v-superman-dawn-of-justice-imax-3d-bengaluru/movie-bang-ET00038215-MT/20160325']
MOVIE = 'batman-v-superman-dawn-of-justice-imax-3d-bengaluru/movie-bang-ET00038215-MT/20160324'
# MOVIE = 'batman-v-superman-dawn-of-justice-imax-3d-bengaluru/movie-bang-ET00038215-MT/20160325'

def send_email(price):
    global BASE_URL

    try:
        s = smtplib.SMTP(SMTP_URL)
        s.starttls()
        s.login(email_user, email_pass)
    except smtplib.SMTPAuthenticationError:
        print("Failed to login")
    else:
        print("Logged in! Composing message..")
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Price Alert - {}".format(price)
        msg["From"] = email_user
        msg["To"] = email_user
        text = "The price is currently {0} !! URL to salepage: {1}".format(price, BASE_URL)
        part = MIMEText(text, "plain")
        msg.attach(part)
        s.sendmail(email_user, email_user, msg.as_string())
        print("Message has been sent.")

while True:
    #item[0] is the item's ASIN while item[1] is that item's maximum price
    r = requests.get(BASE_URL + MOVIE)
    tree = html.fromstring(r.text)
    try:
        print tree.xpath(XPATH_SELECTOR)
        # print movie
        # url = movie.xpath('@href').extract()[0]
        # print url
        # theatre = movie.xpath('.//strong/text()').extract()[0]
        # price = float(tree.xpath(XPATH_SELECTOR)[0].text[1:])
        # print theatre, url
    except IndexError:
        print("Didn't find the 'price' element, trying again")
        continue
    # if price <= item[1]:
    #     print("Price is {}!! Trying to send email.".format(price))
    #     send_email(price)
    #     break
    # else:
    #     print("Price is {}. Ignoring...".format(price))

    print "Sleeping for {} seconds".format(SLEEP_INTERVAL)
    time.sleep(SLEEP_INTERVAL)