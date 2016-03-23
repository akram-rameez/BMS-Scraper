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


BASE_URL = "https://in.bookmyshow.com/buytickets/"
SMTP_URL = "smtp.gmail.com:587"
# XPATH_SELECTOR = '/html/body/section/div/div/ul/li/div/div/div/a/strong'
BASE_XPATH_SELECTOR = '/html/body/section/div/div/ul/li'
#                      /html/body/section/div/div/ul/li /div[2]/div[1]/a
SLEEP_INTERVAL = 10
# MOVIE is the relative link to the movie
MOVIE = 'batman-v-superman-dawn-of-justice-imax-3d-bengaluru/movie-bang-ET00038215-MT/'
# DATE is the date you want it in. Format: YYYYMMDD
DATE = '20160324'

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
    r = requests.get(BASE_URL + MOVIE + DATE)
    tree = html.fromstring(r.text)
    try:

        theatre_names = tree.xpath(BASE_XPATH_SELECTOR + '/@data-name')
        theatre_id = tree.xpath(BASE_XPATH_SELECTOR + '/@data-id')

        for i,val in enumerate(theatre_id):

            # movie_timings = tree.xpath(BASE_XPATH_SELECTOR + '/div[2]/div[@data-online="Y"]/a/@data-showtime-code')
            all_movie_timings = tree.xpath(BASE_XPATH_SELECTOR + '[@data-id="'+val+'"]/div/div/a/@data-showtime-code')
            active_movie_timings = tree.xpath(BASE_XPATH_SELECTOR + '[@data-id="'+val+'"]/div/div[@data-online="Y"]/a/@data-showtime-code')
            # movie_timings = tree.xpath(BASE_XPATH_SELECTOR + '/div[@class="body"]/div/a/@data-showtime-code')
            print val
            for j,jval in enumerate(all_movie_timings):
                if jval in active_movie_timings:
                    print "    "+jval+" Available"
                else:
                    print "    "+jval+" Not Available"
            # movie_timings = tree.xpath(BASE_XPATH_SELECTOR + '/div[@class="body"]/div/a/@data-date-time')
            # theatre_names = tree.xpath(BASE_XPATH_SELECTOR + '/@data-name')
            
        #     movie_timings_links = tree.xpath(BASE_XPATH_SELECTOR + '/div[@class="body"]/div/a/@href')
        #     # for i,val in enumerate(movie_timings):
        #     print movie_timings, movie_timings_links
        # print movie_names
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

    print "----"
    # print "Sleeping for {} seconds".format(SLEEP_INTERVAL)
    time.sleep(SLEEP_INTERVAL)