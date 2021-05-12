import requests #to access the url
from bs4 import BeautifulSoup
import pandas as pd
import smtplib #for email send
import time
from datetime import datetime,timedelta
import json
from lxml import html
import numpy as np
import json

class Investing():

    def __init__(self,firebase,urlF):
        self.firebase = firebase
        self.urlF = urlF

    def df_to_json(self,oldDF):
        result = oldDF.to_json(orient="index")
        parsed = json.loads(result)
        resultDF = self.firebase.put("/investing","tables",parsed)

    def format_columns(self,oldDf):
        oldDf['Starting price'] = oldDf['Starting price'].astype('float').map('{:.4f}'.format)
        oldDf['Starting price (USD)'] = oldDf['Starting price (USD)'].astype('float').map('{:.4f}'.format)
        oldDf['Current value'] = oldDf['Current value'].astype('float').map('{:.4f}'.format)
        oldDf['Delta position'] = oldDf['Delta position'].astype('float').map('{:.4f}'.format)
        oldDf['Selling value'] = oldDf['Selling value'].astype('float').map('{:.4f}'.format)
        oldDf['Income'] = oldDf['Income'].astype('float').map('{:.4f}'.format)
        oldDf['Position'] = oldDf['Position'].astype('float').map('{:.4f}'.format)
        oldDf['Current position'] = oldDf['Current position'].astype('float').map('{:.4f}'.format)
        return oldDf

    def send_email(self,mailFrom,pwd,mailTo,df): #df is the df with the values that changed a lot

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo() #identify itself to the e-mail
        server.starttls()
        server.ehlo()
        server.login(mailFrom,pwd) #user, password: mjhfyerdflugmfvi

        subject = "The price changed a lot!"
        body = "Hey! CHECK THE FILE! The following values:\n\n"
        for name,symbol,old,new in zip(df.Name.unique(),df.Acronym.unique(),df["Current value"].unique(),df.newValue.unique()):
            body = body + "    - " + name + ": " + symbol + " (from " + str(old) + " to " + str(new) + ")\n"
        body = body + "\nhave changed significantly!"
        msg = "Subject: {}\n\n{}".format(subject,body)
        server.sendmail(
            from_addr = mailFrom,
            to_addrs  = mailTo,
            msg = msg
        )

        server.quit()

    #check the old csv file: if new cryptos are added to json, they are added to csv as well
    def check_old_value(self,fileName,json_file):
        cryptos = []
        for j in json_file:
            cryptos.append(json_file[j]["name"])
        oldDf = pd.read_csv(fileName)
        existing_cryptos = oldDf.Name.unique()
        # print(existing_cryptos)
        # print(cryptos)
        
        if len(existing_cryptos)<len(cryptos):
            for c in cryptos:
                if c not in existing_cryptos:
                    for j in json_file:
                        if json_file[j]["name"] == c:
                            tmp = pd.DataFrame([[json_file[j]["name"],\
                                                json_file[j]["symbol"],\
                                                json_file[j]["starting_price"],\
                                                json_file[j]["starting_price"]*json_file[j]["quantity"],\
                                                json_file[j]["quantity"],\
                                                json_file[j]["purchase_date"],\
                                                json_file[j]["value"],\
                                                json_file[j]["last_update_position"]-json_file[j]["yesterday_position"],\
                                                json_file[j]["selling_value"],\
                                                json_file[j]["selling_value"]*json_file[j]["quantity"]-json_file[j]["starting_price"]*json_file[j]["quantity"],\
                                                json_file[j]["value"]*json_file[j]["quantity"]-json_file[j]["starting_price"]*json_file[j]["quantity"],\
                                                json_file[j]["value"]*json_file[j]["quantity"]-json_file[j]["starting_price"]*json_file[j]["quantity"]]],\
                                                columns=["Name","Acronym","Starting price","Starting price (USD)","Quantity","Date","Current value","Delta position","Selling value","Income","Position","Current position"])
                    oldDf = oldDf.append(tmp)
            oldDf['Selling value'] = oldDf['Selling value'].fillna(np.nan)
            # print("CIaoo")
            # print(oldDf[["Name","Acronym","Starting price","Starting price (USD)","Quantity","Date","Current value","Selling value","Income","Position","Current position"]])
            oldDf = self.format_columns(oldDf)
            oldDf[["Name","Acronym","Starting price","Starting price (USD)","Quantity","Date","Current value","Delta position","Selling value","Income","Position","Current position"]].to_csv(fileName,index=False)
            self.df_to_json(oldDf)

        # If you want the code to be sensitive to the changes on csv ==> I wouldn't do it: user can change names ?!
        # else:
        #     for c in cryptos:
        #         for j in json_file:
        #             if json_file[j]["name"] == c:

        return oldDf

    def check_price(self,url,headers,csvFile,oldDf,json_file,delta_perc,mailFrom,mailTo,pwd):
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content,"html.parser")
        # Prints the entire html page
        # print(soup.prettify())
        newValues = pd.DataFrame(columns=["Name","newValue","Delta position"])
        for c in json_file:
            # print(json_file[c]["href"])
            value = float(soup.find(href=json_file[c]["href"]).get_text().replace('.','').replace(',','.'))
            # print(value)
            json_file[c]["value"] = value
            json_file[c]["last_update_position"] = (json_file[c]["value"]-json_file[c]["starting_price"])*json_file[c]['quantity']
            now = datetime.strptime(str(datetime.now()),"%Y-%m-%d  %H:%M:%S.%f")
            # If a day is passed, the position of yesterday is updated with the current one
            if now-datetime.strptime(json_file[c]["yesterday_to_check"],"%Y-%m-%d %H:%M:%S.%f")>=timedelta(days=1):
                json_file[c]["yesterday_position"] = json_file[c]["last_update_position"]
                json_file[c]["yesterday_to_check"] = str(datetime.now())#[:10]
            newValues = newValues.append(pd.DataFrame([[json_file[c]["name"],value,json_file[c]["last_update_position"]-json_file[c]["yesterday_position"]]],columns=["Name","newValue","Delta position"]))

        json.dump(json_file,open("cryptos.json",'w'))
        result = self.firebase.put("/investing","cryptos",json_file)
        oldDf = oldDf.drop("Delta position",axis=1).merge(newValues,on=["Name"],how='left')
        # print(oldDf[["newValue","Current value"]])
        oldDf['Difference Percentage'] = abs((oldDf['newValue']-oldDf['Current value'].astype("float")))/oldDf['Current value'].astype("float")
        oldDf['flag'] = 0
        oldDf['flag'].mask(oldDf['Difference Percentage']>delta_perc,1,inplace=True)
        if 1 in oldDf.flag.unique():
            print("Values have changed significantly! See the e-mail for more details.")
            jumpedDf = oldDf[oldDf['flag']==1]
            self.send_email(mailFrom,pwd,mailTo,jumpedDf)
            print("E-mail sent!")
        oldDf.drop(["Current value",'Difference Percentage','flag'],axis=1,inplace=True)
        oldDf.rename(columns={"newValue":"Current value"},inplace=True)
        oldDf["Position"] = oldDf["Current value"].astype("float")*oldDf["Quantity"].astype("float") - oldDf["Starting price"].astype("float")*oldDf["Quantity"].astype("float")
        oldDf["Current position"] = oldDf["Current value"].astype("float")*oldDf["Quantity"].astype("float") - oldDf["Starting price"].astype("float")*oldDf["Quantity"].astype("float")
        oldDf = self.format_columns(oldDf)
        oldDf[["Name","Acronym","Starting price","Starting price (USD)","Quantity","Date","Current value","Delta position","Selling value","Income","Position","Current position"]].to_csv(csvFile,index=False)
        self.df_to_json(oldDf)
        # I want to track the info in here
        # value = float(soup.find(href='/crypto/currency-pairs?c1=189&c2=12').get_text().replace('.','').replace(',','.'))
        return value