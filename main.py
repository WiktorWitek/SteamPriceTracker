import requests
from bs4 import BeautifulSoup
import smtplib

# Steam market item url
URL = "https://steamcommunity.com/market/listings/730/%E2%98%85%20Butterfly%20Knife%20%7C%20" \
      "Crimson%20Web%20%28Field-Tested%29"

response = requests.get(URL)
html_text = response.text

soup = BeautifulSoup(html_text, "html.parser")

# Finding cheapest item listed on steam market
cheapest_item = soup.findAll(name="span", class_="market_listing_price market_listing_price_with_fee")[0]
item_value_only = cheapest_item.text.strip().replace("$", "")
slicer = item_value_only.find("USD")
item_value_only = item_value_only[:slicer-1].replace(",", "")
item_value_only = int(item_value_only[:-3])

# Set your target price in USD
TARGET = 1380 #USD


# Send email notification if target is higher than item price
login = ""  # email address to sent email from
password = ""  # email app password


item_name = soup.findAll(name="span", id="listing_4380372458404328215_name")[0].text


if item_value_only <= TARGET:
    with smtplib.SMTP("smtp.gmail.com") as email:
          email.starttls()
          email.login(login, password)
          email.sendmail(from_addr=login,
                         to_addrs="", # address to recive email
                         msg=f"Subject:{item_name[1:]} price update\n\nThe item that you are looking ({item_name[1:]}) for is listed on steam market for {item_value_only}$\n"
                                                                                        f"Check it out on: {URL}")

