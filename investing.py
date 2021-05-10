import requests #to access the url
from bs4 import BeautifulSoup
import pandas as pd
import smtplib #for email send
import time
from datetime import datetime,timedelta
import json
from lxml import html
import numpy as np

def format_columns(oldDf):
    oldDf['Starting price'] = oldDf['Starting price'].astype('float').map('{:.4f}'.format)
    oldDf['Starting price (USD)'] = oldDf['Starting price (USD)'].astype('float').map('{:.4f}'.format)
    oldDf['Current value'] = oldDf['Current value'].astype('float').map('{:.4f}'.format)
    oldDf['Delta position'] = oldDf['Delta position'].astype('float').map('{:.4f}'.format)
    oldDf['Selling value'] = oldDf['Selling value'].astype('float').map('{:.4f}'.format)
    oldDf['Income'] = oldDf['Income'].astype('float').map('{:.4f}'.format)
    oldDf['Position'] = oldDf['Position'].astype('float').map('{:.4f}'.format)
    oldDf['Current position'] = oldDf['Current position'].astype('float').map('{:.4f}'.format)
    return oldDf

def send_email(mailFrom,pwd,mailTo,df): #df is the df with the values that changed a lot

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo() #identify itself to the e-mail
    server.starttls()
    server.ehlo()
    server.login(mailFrom,pwd) #user, password: mjhfyerdflugmfvi

    subject = "The price changed a lot!"
    body = "Hey! CHECK THE FILE! The following values:\n\n"
    for name,symbol,old,new in zip(df.Name.unique(),df.Acronym.unique(),df.Value.unique(),df.newValue.unique()):
        body = body + "    - " + name + ": " + symbol + " (from " + str(old) + " to " + str(new) + ")\n"
    body = body + "\nhave changed significantly!"
    msg = "Subject: {}\n\n{}".format(subject,body)
    server.sendmail(
        from_addr = mailFrom,
        to_addrs  = mailTo,
        msg = msg
    )

    server.quit()

def add_new_crypto(url,headers):
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,"html.parser")

    start = input("Do you want to add a new cryptovalue? (y/n) ")
    tot_json = json.load(open("data.json"))
    existing = tot_json["cryptos"]
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
        prova = soup.find("table").find('tbody').find_all('tr')
        for row in prova:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if (symbolC in cols) and (nameC in cols):
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
        tot_json["cryptos"] = existing
        json.dump(tot_json,open("data.json",'w'))
        start = input("Do you still want to add more cryptovalues? (y/n) ")
        print("\n")
    return tot_json

#check the old csv file: if new cryptos are added to json, they are added to csv as well
def check_old_value(fileName,json_file):
    cryptos = []
    for j in json_file["cryptos"]:
        cryptos.append(json_file["cryptos"][j]["name"])
    oldDf = pd.read_csv(fileName)
    existing_cryptos = oldDf.Name.unique()
    # print(existing_cryptos)
    # print(cryptos)
    
    if len(existing_cryptos)<len(cryptos):
        for c in cryptos:
            if c not in existing_cryptos:
                for j in json_file["cryptos"]:
                    if json_file["cryptos"][j]["name"] == c:
                        tmp = pd.DataFrame([[json_file["cryptos"][j]["name"],\
                                            json_file["cryptos"][j]["symbol"],\
                                            json_file["cryptos"][j]["starting_price"],\
                                            json_file["cryptos"][j]["starting_price"]*json_file["cryptos"][j]["quantity"],\
                                            json_file["cryptos"][j]["quantity"],\
                                            json_file["cryptos"][j]["purchase_date"],\
                                            json_file["cryptos"][j]["value"],\
                                            json_file["cryptos"][j]["last_update_position"]-json_file["cryptos"][j]["yesterday_position"],\
                                            json_file["cryptos"][j]["selling_value"],\
                                            json_file["cryptos"][j]["selling_value"]*json_file["cryptos"][j]["quantity"]-json_file["cryptos"][j]["starting_price"]*json_file["cryptos"][j]["quantity"],\
                                            json_file["cryptos"][j]["value"]*json_file["cryptos"][j]["quantity"]-json_file["cryptos"][j]["starting_price"]*json_file["cryptos"][j]["quantity"],\
                                            json_file["cryptos"][j]["value"]*json_file["cryptos"][j]["quantity"]-json_file["cryptos"][j]["starting_price"]*json_file["cryptos"][j]["quantity"]]],\
                                            columns=["Name","Acronym","Starting price","Starting price (USD)","Quantity","Date","Current value","Delta position","Selling value","Income","Position","Current position"])
                oldDf = oldDf.append(tmp)
        oldDf['Selling value'] = oldDf['Selling value'].fillna(np.nan)
        # print("CIaoo")
        # print(oldDf[["Name","Acronym","Starting price","Starting price (USD)","Quantity","Date","Current value","Selling value","Income","Position","Current position"]])
        oldDf = format_columns(oldDf)
        oldDf[["Name","Acronym","Starting price","Starting price (USD)","Quantity","Date","Current value","Delta position","Selling value","Income","Position","Current position"]].to_csv(fileName,index=False)
    # If you want the code to be sensitive to the changes on csv ==> I wouldn't do it: user can change names ?!
    # else:
    #     for c in cryptos:
    #         for j in json_file:
    #             if json_file[j]["name"] == c:

    return oldDf

def check_price(url,headers,csvFile,oldDf,json_file,delta_perc,mailFrom,mailTo,pwd):
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,"html.parser")
    # Prints the entire html page
    # print(soup.prettify())
    newValues = pd.DataFrame(columns=["Name","newValue","Delta position"])
    for c in json_file["cryptos"]:
        # print(json_file[c]["href"])
        value = float(soup.find(href=json_file["cryptos"][c]["href"]).get_text().replace('.','').replace(',','.'))
        # print(value)
        json_file["cryptos"][c]["value"] = value
        json_file["cryptos"][c]["last_update_position"] = (json_file["cryptos"][c]["value"]-json_file["cryptos"][c]["starting_price"])*json_file["cryptos"][c]['quantity']
        now = datetime.strptime(str(datetime.now()),"%Y-%m-%d  %H:%M:%S.%f")
        # If a day is passed, the position of yesterday is updated with the current one
        if now-datetime.strptime(json_file["cryptos"][c]["yesterday_to_check"],"%Y-%m-%d %H:%M:%S.%f")>=timedelta(days=1):
            json_file["cryptos"][c]["yesterday_position"] = json_file["cryptos"][c]["last_update_position"]
            json_file["cryptos"][c]["yesterday_to_check"] = str(datetime.now())#[:10]
        newValues = newValues.append(pd.DataFrame([[json_file["cryptos"][c]["name"],value,json_file["cryptos"][c]["last_update_position"]-json_file["cryptos"][c]["yesterday_position"]]],columns=["Name","newValue","Delta position"]))

    json.dump(json_file,open("data.json",'w'))
    oldDf = oldDf.drop("Delta position",axis=1).merge(newValues,on=["Name"],how='left')
    # print(oldDf[["newValue","Current value"]])
    oldDf['Difference Percentage'] = abs((oldDf['newValue']-oldDf['Current value'].astype("float")))/oldDf['Current value'].astype("float")
    oldDf['flag'] = 0
    oldDf['flag'].mask(oldDf['Difference Percentage']>delta_perc,1,inplace=True)
    if 1 in oldDf.flag.unique():
        print("Values have changed significantly! See the e-mail for more details.")
        jumpedDf = oldDf[oldDf['flag']==1]
        send_email(mailFrom,pwd,mailTo,jumpedDf)
        print("E-mail sent!")
    oldDf.drop(["Current value",'Difference Percentage','flag'],axis=1,inplace=True)
    oldDf.rename(columns={"newValue":"Current value"},inplace=True)
    oldDf["Position"] = oldDf["Current value"].astype("float")*oldDf["Quantity"].astype("float") - oldDf["Starting price"].astype("float")*oldDf["Quantity"].astype("float")
    oldDf["Current position"] = oldDf["Current value"].astype("float")*oldDf["Quantity"].astype("float") - oldDf["Starting price"].astype("float")*oldDf["Quantity"].astype("float")
    oldDf = format_columns(oldDf)
    oldDf[["Name","Acronym","Starting price","Starting price (USD)","Quantity","Date","Current value","Delta position","Selling value","Income","Position","Current position"]].to_csv(csvFile,index=False)
    # I want to track the info in here
    # value = float(soup.find(href='/crypto/currency-pairs?c1=189&c2=12').get_text().replace('.','').replace(',','.'))
    return value

def choose_frequency():
    print("Choose the frequency of the updates.")
    print("Types of time: s (seconds), m (minutes), h (hours)")
    print("Examples:\n   - 10 s: every 10 seconds the data will be updated;\n   - 5 m: every 5 minutes the data will be updated;\n   - 3 h: every 3 hours the data will be updated.")
    print("")
    f_input = input("Insert the frequency: ")
    f_amount = int(f_input.split(" ")[0])
    f_type = f_input.split(" ")[1]
    return f_amount,f_type

def choose_delta():
    print("Insert the percentage of change you want to be notified for.")
    print("Examples:\n    - 5: it means that if values change by 5% you will be notified by e-mail;\n    - 25: it means that if values change by 25% you will be notified by e-mail.\n")
    delta = float(input("Insert the change in percentage: ").replace(" ",""))/100
    return delta

def main(url,headers,mailFrom,mailTo,pwd,csvFile,delta_perc,json_file):
    oldDf = check_old_value(csvFile,json_file)
    check_price(url,headers,csvFile,oldDf,json_file,delta_perc,mailFrom,mailTo,pwd)


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
f_amount, f_type = choose_frequency()
print("") 
delta_perc = choose_delta()
print("")
json_file = add_new_crypto(url,headers)

while True:
    print("")
    print("Current date: ",str(datetime.now())[:-7],"\n")
    main(url,headers,mailFrom,mailTo,pwd,csvFile,delta_perc,json_file)
    print("\n")
    if f_amount==1:
        print("Sleeping for {} {}...".format(str(f_amount),freq_msg_dic_singolar[f_type]))
    else:
        print("Sleeping for {} {}...".format(str(f_amount),freq_msg_dic_plural[f_type]))
    time.sleep(f_amount*freq_amount_dic[f_type]) #one minute: 60, one hour: 60*60