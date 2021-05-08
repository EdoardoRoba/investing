import requests #to access the url
from bs4 import BeautifulSoup
import pandas as pd
import smtplib #for email send
import time
from datetime import datetime
import json

def send_email(mailFrom,pwd,mailTo,df): #df is the df with the values that changed a lot

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo() #identify itself to the e-mail
    server.starttls()
    server.ehlo()
    server.login(mailFrom,pwd) #user, password: mjhfyerdflugmfvi

    subject = "The price changed a lot!"
    body = "Hey! CHECK THE FILE! The following values:\n\n"
    for name,symbol,old,new in zip(df.Name.unique(),df.Symbol.unique(),df.Value.unique(),df.newValue.unique()):
        body = body + "    - " + name + ": " + symbol + " (from " + str(old) + " to " + str(new) + ")\n"
    body = body + "\nhave changed significantly!"
    msg = "Subject: {}\n\n{}".format(subject,body)
    server.sendmail(
        from_addr = mailFrom,
        to_addrs  = mailTo,
        msg = msg
    )

    server.quit()

def add_new_crypto(url,headers,i):
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,"html.parser")

    if i == 0:
        start = input("Do you want to add a new cryptovalue? (y/n) ")
        existing = json.load(open("data.json"))
        print("\n")
        last_element = max([int(k[1:]) for k in existing.keys()])

        while start=="y":
            dic = {}
            nameC = input("Insert the name of the crypto value: ")
            symbolC = input("Insert the symbol of the crypto value: ")
            href = input("Insert the href of the crypto value: ")
            print("\n")
            dic["name"] = nameC
            dic["symbol"] = symbolC
            dic["href"] = href # "/crypto/currency-pairs?c1=189&amp;c2=12" #TO CHANGE WHENEVER A CRYPTOVALUE IS ADDED
            dic["value"] = float(soup.find(href=href).get_text().replace('.','').replace(',','.'))
            last_element += 1
            existing["c"+str(last_element)] = dic
            json.dump(existing,open("data.json",'w'))
            start = input("Do you still want to add more cryptovalues? (y/n) ")
    else:
        existing = json.load(open("data.json"))
    return existing

#check the old csv file: if new cryptos are added to json, they are added to csv as well
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
    return oldDf

def check_price(url,headers,csvFile,oldDf,json_file,delta_perc,mailFrom,mailTo,pwd):
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,"html.parser")
    # Prints the entire html page
    # print(soup.prettify())
    newValues = pd.DataFrame(columns=["Name","newValue"])
    for c in json_file:
        # print(json_file[c]["href"])
        value = float(soup.find(href=json_file[c]["href"]).get_text().replace('.','').replace(',','.'))
        # print(value)
        json_file[c]["value"] = value
        newValues = newValues.append(pd.DataFrame([[json_file[c]["name"],value]],columns=["Name","newValue"]))

    json.dump(json_file,open("data.json",'w'))
    oldDf = oldDf.merge(newValues,on=["Name"],how='left')
    oldDf['Difference Percentage'] = abs((oldDf['newValue']-oldDf['Value']))/oldDf['Value']
    oldDf['flag'] = 0
    oldDf['flag'].mask(oldDf['Difference Percentage']>delta_perc,1,inplace=True)
    if 1 in oldDf.flag.unique():
        print("Values have changed significantly! See the e-mail for more details.")
        jumpedDf = oldDf[oldDf['flag']==1]
        send_email(mailFrom,pwd,mailTo,jumpedDf)
        print("E-mail sent!")
    oldDf.drop(["Value",'Difference Percentage','flag'],axis=1,inplace=True)
    oldDf.rename(columns={"newValue":"Value"},inplace=True)
    oldDf.to_csv(csvFile,index=False)
    # I want to track the info in here
    # value = float(soup.find(href='/crypto/currency-pairs?c1=189&c2=12').get_text().replace('.','').replace(',','.'))
    return value

def main(url,headers,mailFrom,mailTo,pwd,csvFile,delta_perc,i):
    json_file = add_new_crypto(url,headers,i)
    oldDf = check_old_value(csvFile,json_file)
    check_price(url,headers,csvFile,oldDf,json_file,delta_perc,mailFrom,mailTo,pwd)


url =  'https://it.investing.com/crypto/currencies'
headers = {"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
csvFile = 'stock_price.csv'
delta_perc = 0.0005
mailFrom = 'investing.notification.bot@gmail.com'
# mailTo = 'federico.masci96@gmail.com'
mailTo = 'recensioni.culinarieIT@gmail.com'
pwd = 'loxrhejcrnbiafbd'
i = 0

while True:
    print("\n")
    print("Current date: ",datetime.now(),"\n")
    main(url,headers,mailFrom,mailTo,pwd,csvFile,delta_perc)
    print("\n")
    print("Sleeping for one hour...\n")
    time.sleep(60*60)