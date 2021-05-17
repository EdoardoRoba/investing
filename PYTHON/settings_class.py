import requests #to access the url
from bs4 import BeautifulSoup
import pandas as pd
import smtplib #for email send
import time
from datetime import datetime,timedelta
import json
from lxml import html
import numpy as np

class Settings():

    def __init__(self,firebase,urlF):
        self.firebase = firebase
        self.urlF = urlF

    def df_to_json(self,oldDF):
        df = oldDF.copy()
        df.rename(columns={"Name":"name",\
                            "Acronym":"acronym",
                            "Starting price":"starting_price",
                            "Starting price (USD)":"starting_price_usd",
                            "Quantity":"quantity",
                            "Date":"date",
                            "Current value":"current_value",
                            "Delta position":"delta_position",
                            "Selling value":"selling_value",
                            "Income":"income",
                            "Position":"position",
                            "Current position":"current_position"
                            },inplace=True)
        result = df.to_json(orient="index")
        parsed = json.loads(result)
        resultDF = self.firebase.put("/investing","tables",parsed)

    def choose_frequency(self):
        # print("Choose the frequency of the updates.")
        # print("Types of time: s (seconds), m (minutes), h (hours)")
        # print("Examples:\n   - 10 s: every 10 seconds the data will be updated;\n   - 5 m: every 5 minutes the data will be updated;\n   - 3 h: every 3 hours the data will be updated.")
        # print("")
        # f_input = input("Insert the frequency: ")
        # f_amount = int(f_input.split(" ")[0])
        # f_type = f_input.split(" ")[1]
        f_amount = 10
        f_type = 's'
        return f_amount,f_type

    def choose_delta(self):
        # print("Insert the percentage of change you want to be notified for.")
        # print("Examples:\n    - 5: it means that if values change by 5% you will be notified by e-mail;\n    - 25: it means that if values change by 25% you will be notified by e-mail.\n")
        # delta = float(input("Insert the change in percentage: ").replace(" ",""))/100
        delta = 0.1
        return delta

    def add_new_crypto(self,url,headers):
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content,"html.parser")

        # start = input("Do you want to add a new cryptovalue? (y/n) ")
        start = "n"

        existing = json.load(open("cryptos.json"))
        print("\n")
        last_element = max([int(k[1:]) for k in existing.keys()])

        while start=="y":
            dic = {}
            nameC = input("Insert the name of the crypto value: ")
            symbolC = input("Insert the symbol of the crypto value: ")
            # href = input("Insert the href of the crypto value: ")
            dic["quantity"] = float(input("Insert the quantity for this cryptovalue: "))
            print("\n")
            dic["name"] = nameC
            dic["symbol"] = symbolC
            # dic["href"] = href # "/crypto/currency-pairs?c1=189&amp;c2=12" #TO CHANGE WHENEVER A CRYPTOVALUE IS ADDED
            prova = soup.find("table").find('tbody').find_all('tr',limit=1000)
            for row in prova:
                cols = row.find_all('td',limit=1000)
                cols = [ele.text.strip() for ele in cols]
                # print(symbolC)
                # print(nameC)
                # print(cols)
                if (symbolC in cols) or (nameC in cols): #  and (nameC in cols)
                    # print(row)
                    webpage = html.fromstring(str(row))
                    dic["href"] = webpage.xpath('//a/@href')[1]
                    # print(webpage.xpath('//a/@href')[1])
            dic["value"] = float(soup.find(href=dic["href"]).get_text().replace('.','').replace(',','.'))
            dic["starting_price"] = dic["value"]
            dic["purchase_date"] = str(datetime.now())[:10]
            dic["selling_value"] = 0
            # Check if the date is a day after the last position computation
            dic["yesterday_to_check"] = str(datetime.now())#[:10]
            dic["yesterday_position"] = (dic["value"]-dic["starting_price"])*dic['quantity']
            dic["last_update_position"] = (dic["value"]-dic["starting_price"])*dic['quantity']
            last_element += 1
            # print(last_element)
            existing["c"+str(last_element)] = dic
            json.dump(existing,open("cryptos.json",'w'))
            result = self.firebase.put("/investing","cryptos",existing)
            start = input("Do you still want to add more cryptovalues? (y/n) ")
            print("\n")
        return existing