import requests #to access the url
from bs4 import BeautifulSoup
import pandas as pd
import smtplib #for email send
import time
from datetime import datetime
import json

url =  'https://it.investing.com/crypto/'
headers = {"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}

page = requests.get(url,headers=headers)
soup = BeautifulSoup(page.content,"html.parser")

# Prints the entire html page
# print(soup.prettify())

# I want to track the info in here
value = soup.find(title="Bitcoin")#.get_text()
print(value)