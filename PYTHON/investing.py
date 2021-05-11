import requests #to access the url
from bs4 import BeautifulSoup
import pandas as pd
import smtplib #for email send
import time
from datetime import datetime,timedelta
import json
from lxml import html
import numpy as np
from firebase import firebase
from investing_class import Investing
from settings_class import Settings

urlF = "https://investing-82e20-default-rtdb.firebaseio.com/"
firebase = firebase.FirebaseApplication(urlF,None)

def main(url,headers,mailFrom,mailTo,pwd,csvFile,delta_perc,json_file,investing):
    oldDf = investing.check_old_value(csvFile,json_file)
    investing.check_price(url,headers,csvFile,oldDf,json_file,delta_perc,mailFrom,mailTo,pwd)

investing = Investing(firebase,urlF)
setting = Settings(firebase,urlF)
url =  'https://it.investing.com/crypto/currencies'
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"}
csvFile = 'stock_price.csv'
mailFrom = 'investing.notification.bot@gmail.com'
# mailTo = 'federico.masci96@gmail.com'
mailTo = 'recensioni.culinarieIT@gmail.com'
pwd = 'loxrhejcrnbiafbd'
freq_amount_dic = {"s":1,"m":60,"h":60*60}
freq_msg_dic_singolar = {"s":"second","m":"minute","h":"hour"}
freq_msg_dic_plural = {"s":"seconds","m":"minutes","h":"hours"}
f_amount, f_type = setting.choose_frequency()
print("") 
delta_perc = setting.choose_delta()
print("")
json_file = setting.add_new_crypto(url,headers)

while True:
    print("")
    print("Current date: ",str(datetime.now())[:-7],"\n")
    main(url,headers,mailFrom,mailTo,pwd,csvFile,delta_perc,json_file,investing)
    print("\n")
    if f_amount==1:
        print("Sleeping for {} {}...".format(str(f_amount),freq_msg_dic_singolar[f_type]))
    else:
        print("Sleeping for {} {}...".format(str(f_amount),freq_msg_dic_plural[f_type]))
    time.sleep(f_amount*freq_amount_dic[f_type]) #one minute: 60, one hour: 60*60