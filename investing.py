import requests #to access the url
from bs4 import BeautifulSoup
import pandas as pd
import smtplib #for email send
import time
from datetime import datetime
import json

def send_email(mailFrom,pwd,mailTo,criptoName,criptoSymbol,oldValue,newValue):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo() #identify itself to the e-mail
    server.starttls()
    server.ehlo()
    server.login(mailFrom,pwd) #user, password: mjhfyerdflugmfvi

    subject = "The price changed a lot!"
    body = "Hey! CHECK THE FILE! The value of {} ({}) has changed significantly! From {} to {}!".format(criptoName,criptoSymbol,oldValue,newValue)
    msg = "Subject: {}\n\n{}".format(subject,body)
    server.sendmail(
        from_addr = mailFrom,
        to_addrs  = mailTo,
        msg = msg
    )

    server.quit()

def add_new_crypto(url,headers):
    start = input("Do you want to add a new cryptovalue? (y/n)")
    existing = json.load(open("data.json"))
    last_element = max([int(k[1:]) for k in existing.keys()])

    while start=="y":
        dic = {}
        nameC = input("Insert the name of the crypto value: ")
        symbolC = input("Insert the symbol of the crypto value: ")
        dic["name"] = nameC
        dic["symbol"] = symbolC
        dic["href"] = "" # "/crypto/currency-pairs?c1=189&amp;c2=12" #TO CHANGE WHENEVER A CRYPTOVALUE IS ADDED
        dic["value"] = 0 #float(soup.find(href='/crypto/currency-pairs?c1=189&c2=12').get_text().replace('.','').replace(',','.'))
        last_element += 1
        existing["c"+str(last_element)] = dic
        json.dump(existing,open("data.json",'w'))
        start = input("Do you still want to add more cryptovalues? (y/n)")

    return existing

#chck the old csv file: if new cryptos are added to json, they are added to csv as well
def check_old_value(fileName,json_file):
    cryptos = []
    for j in json_file:
        cryptos.append(json_file[j]["name"])
    oldDf = pd.read_csv(fileName)
    existing_cryptos = oldDf.Name.unique()
    if len(existing_cryptos)<len(cryptos):
        for c in cryptos:
            if c not in existing_cryptos:
                for j in json_file:
                    if json_file[j]["name"] == c:
                        tmp = pd.DataFrame([[json_file[j]["name"],json_file[j]["symbol"],json_file[j]["value"]]],columns=["Name","Symbol","Value"])
                oldDf = oldDf.append(tmp)
        oldDf.to_csv(fileName,index=False)                     

    # oldDF = pd.read_excel(fileName)
    # CAMBIARE SE CI SONO TANTI VALORI
    # criptoName = oldDf.Name.unique()[0]
    # criptoSymbol = oldDf.Symbol.unique()[0]
    # oldValue = float(oldDf.Value.unique()[0])
    # return criptoName,criptoSymbol,oldValue
    return oldDf

def check_price(url,headers,oldDf,json_file):
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,"html.parser")
    # Prints the entire html page
    # print(soup.prettify())
    values = pd.DataFrame(columns=["Names","newValue"])
    for c in json_file:
        print(json_file[c]["href"])
        value = float(soup.find(href=json_file[c]["href"]).get_text().replace('.','').replace(',','.'))
        # print(value)
        values = values.append(pd.DataFrame([[json_file[c]["name"],value]],columns=["Names","newValue"]))
    print(values)
    # I want to track the info in here
    # value = float(soup.find(href='/crypto/currency-pairs?c1=189&c2=12').get_text().replace('.','').replace(',','.'))
    return value


url =  'https://it.investing.com/crypto/currencies'
headers = {"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
csvFile = 'stock_price.csv'

json_file = add_new_crypto(url,headers)

oldDf = check_old_value(csvFile,json_file)

check_price(url,headers,oldDf,json_file)