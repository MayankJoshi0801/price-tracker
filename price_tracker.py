from os import replace
import requests
import time
import schedule
from bs4 import BeautifulSoup
from requests.api import head
import smtplib

URL = input("Enter your Url\n")
base_price = int(input("what should be the minimum price\n"))

# URL = ("https://www.amazon.in/dp/B08R3YVRRB/ref=syn_sd_onsite_desktop_197?psc=1&pd_rd_plhdr=t&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyUEUwUTQwUkNOSUI0JmVuY3J5cHRlZElkPUEwNDAzMzk0Mk1BU01YTlRYMEtCWSZlbmNyeXB0ZWRBZElkPUEwMjQ0Njg2RkRZVDc3ODg5VjZZJndpZGdldE5hbWU9c2Rfb25zaXRlX2Rlc2t0b3AmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl")

headers = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    
    try:
        price = soup.find(id="priceblock_ourprice").get_text()
    except:
        price = soup.find(id = "priceblock_dealprice").get_text()

    converted_price = (price[0:-3])
    replaced_price = converted_price.replace(',', '')
    replaced_price2 = replaced_price.replace('₹', '')

    final_price = float(replaced_price2)

    print(title)
    print(final_price)

    if (final_price < base_price):
        send_mail()

def send_mail():
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    senders_mail = 'mpstestemail10@gmail.com'
    rec_mail = 'joshimayank08012007@gmail.com'
    password = 'modernpublic'

    server.login("mpstestemail10@gmail.com", "modernpublic")
    print("login succesful")

    subject = 'Price Fell Down!!'
    body = 'Check the link :-'+ URL
                    
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(senders_mail, rec_mail, msg)
    print("E-mail is sent")

    server.quit()

# check_price()
schedule.every(3).hours.do(check_price)
# schedule.every().hour.do(check_price)

while 1:
    schedule.run_pending()
    time.sleep(1)
