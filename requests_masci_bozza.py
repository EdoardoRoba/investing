import requests #to access the url
from bs4 import BeautifulSoup
import pandas as pd
import smtplib #for email send
import time
from datetime import datetime

def check_price(url,headers):
    page = requests.get(url,headers=headers)

    soup = BeautifulSoup(page.content,"html.parser")

    # Prints the entire html page
    # print(soup.prettify())

    # I want to track the info in here
    value = float(soup.find(href='/crypto/currency-pairs?c1=189&c2=12').get_text().replace('.','').replace(',','.'))
    return value

def check_old_value(fileName):
    oldDf = pd.read_csv(fileName)
    # oldDF = pd.read_excel(fileName)
    # CAMBIARE SE CI SONO TANTI VALORI
    criptoName = oldDf.Name.unique()[0]
    criptoSymbol = oldDf.Symbol.unique()[0]
    oldValue = float(oldDf.Value.unique()[0])
    return criptoName,criptoSymbol,oldValue

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

def check_values(criptoName,criptoSymbol,oldValue,newValue,mailFrom,pwd,mailTo,delta):

    print("Old value: ",oldValue)
    print("New value: ",newValue)

    if newValue!=oldValue:
        df = pd.DataFrame([[criptoName,criptoSymbol,newValue]],columns=["Name","Symbol","Value"])
        df.to_csv("stock_price.csv",index=False)
        df.to_excel("stock_price.xlsx")
        if abs(newValue-oldValue)>delta:
            print("Wow! Strong change in {} ({}) value! Sending an e-mail to: ".format(criptoName,criptoSymbol), mailTo)
            send_email(mailFrom,pwd,mailTo,criptoName,criptoSymbol,oldValue,newValue)
            print("E-mail sent!")

def main(url,headers,mailFrom,mailTo,pwd,csvFile,delta):

    criptoName,criptoSymbol,oldValue = check_old_value(csvFile)

    newValue = check_price(url,headers)

    check_values(criptoName,criptoSymbol,oldValue,newValue,mailFrom,pwd,mailTo,delta)

url =  'https://it.investing.com/crypto/currencies'
headers = {"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
mailFrom = 'investing.notification.bot@gmail.com'
# mailTo = 'federico.masci96@gmail.com'
mailTo = 'recensioni.culinarieIT@gmail.com'
pwd = 'loxrhejcrnbiafbd'
csvFile = 'stock_price.csv'
delta = 5

while True:
    print("\n")
    print("Current date: ",datetime.now())
    main(url,headers,mailFrom,mailTo,pwd,csvFile,delta)
    print("\n\n")
    time.sleep(60*60)